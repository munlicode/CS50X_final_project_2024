from openai import OpenAI
import os, math, time, logging
import json
from dotenv import load_dotenv

from response_formats import CompositeFormat
from helpers import overwrite_env_variable

load_dotenv()

def create_assistant(client):
    try:
        name = os.getenv("ASSISTANT_NAME")
        if not name:
            name = input("Enter the name of the assistant: ").strip()
            overwrite_env_variable("ASSISTANT_NAME", name)

        model = os.getenv("ASSISTANT_MODEL")
        if not model:
            model = input("Enter the model: ")
            overwrite_env_variable("ASSISTANT_MODEL", model)

        instructions_path = os.getenv("ASSISTANT_INSTRUCTIONS_PATH")
        
        if not instructions_path:
            instructions_path = input("Enter text file with instructions(full PATH): ")
            overwrite_env_variable("ASSISTANT_INSTRUCTIONS_PATH", instructions_path)     
        try:
            with open(instructions_path, 'r') as file:
                instructions = file.read()
                file.close()
        except Exception as e:
            print(f"Error reading file: {e}")
        
        tools_path = os.getenv("ASSISTANT_TOOLS_PATH")
        
        if not tools_path:
            tools = [
                {
                "type": "function",
                "function": {
                    "name": "plot_linear_equation",
                    "description": "Plots the line y = mx + b and shows the graph with labels.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "m": {
                                "type": "number",
                                "description": "The slope of the line."
                            },
                            "b": {
                                "type": "number",
                                "description": "The y-intercept of the line."
                            },
                            "min_x": {
                                "type": "number",
                                "description": "The minimum x value to plot." 
                            },
                            "max_x": {
                                "type": "number",
                                "description": "The maximum x value to plot."
                        },
                        },
                        "required": ["m", "b"]
                    }
                
                },
            }]
        else:
            try:
                    with open(tools_path, 'r') as file:
                        tools = file.read()
                        file.close()
            except Exception as e:
                print(f"Error reading file: {e}")
        
        response_format = CompositeFormat.model_json_schema()
        
        assistant = client.beta.assistants.create(
            name=name,
            model=model,
            instructions=instructions,
            tools=tools,
            response_format={
           'type': 'json_schema',
           'json_schema': {
                "name":"composite_response", 
                "schema": response_format
              }
         },
        )
        overwrite_env_variable("ASSISTANT_ID", assistant.id)
        return assistant.id
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def conversation(list_text):    
    try:
        if not os.path.exists(".env"):
            with open(".env", "w") as f:
                pass
            
        # Load the API key from the environment
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            api_key = input("Enter your OpenAI API key: ").strip()
            overwrite_env_variable("OPENAI_API_KEY", api_key)
            
        client = OpenAI(api_key=api_key)

        # Load the assistant ID from the sqlite database
        assistant_id = os.getenv("ASSISTANT_ID")
        if not assistant_id:
            assistant_id = create_assistant(client)

        # create a thread
        thread = client.beta.threads.create()    
        logging.info(f"Thread created with id: {thread.id}")
        
        # Start the conversation
        while True:
            message = input("You: ")
            if message.lower() == "exit":
                return 
            
            list_text.append(f"User: {message}\n")
            
            response = generate_response(message=message, assistant_id=assistant_id, thread_id=thread.id, client=client)
            
            list_text.append(f"Assistant:\n{response}\n")
            
            if response:
                print(f"Assistant: {response}")
            else:
                print("Assistant: I'm sorry, I don't understand.")

    except EOFError or KeyboardInterrupt:
        return "You're back to Main Menu." 
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return "Sorry, I encountered an error. Please try again later." 

def generate_response(message, assistant_id, thread_id, client):
    try:    
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message,
        )
        # Create and run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )
        
        # Wait for response (with timeout)
        start_time = time.time()
        generate_time = os.getenv("GENERATE_TIME")
        if not generate_time:
            generate_time = 60
        
        while time.time() - start_time < generate_time:   
            run = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

            if run.status == 'completed':

                messages = client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                message_content = messages.data[0].content[0].text
                
                # Clean up annotations
                annotations = message_content.annotations
                
                for annotation in annotations:
                    message_content.value = message_content.value.replace(
                        annotation.text, ''
                    )
                
                generated_response = json.loads(message_content.value)

                if generated_response['response']['type'] == "explanation":
                    return generated_response['response']['explanation']
                
                elif generated_response['response']['type'] == "quick-answer":
                    return generated_response['response']['answer']
                
                elif generated_response['response']['type'] == "step-by-step":
                    response = ""  
                    for num, step in enumerate(generated_response['response']['steps'], start=1):
                        response += f"Step {num}. {step['explanation']}\n      {step['output']}\n\n"
                    
                    response += generated_response['response']['final_answer']
                    return response
                
                else:
                    return message_content.value

            if run.status == 'failed':
                logging.error(run.error)
                # Break inner loop to trigger retry
                return None

            if run.status == 'requires_action':
                handle_tool_calls(run, client, thread_id)
                    
        return None

    except Exception as e:
        logging(f"Error: {str(e)}")
        return None
    
def handle_tool_calls(run, client, thread_id):
    for tool_call in run.required_action.submit_tool_outputs.tool_calls:
        try:
            if tool_call.function.name == "plot_linear_equation":
                from tools import plot_linear_equation
                arguments = json.loads(tool_call.function.arguments)
                output = plot_linear_equation(
                    arguments["m"],
                    arguments["b"], 
                    arguments["min_x"],
                    arguments["max_x"]
                )
                
            if output is not None:
                client.beta.threads.runs.submit_tool_outputs(
                    thread_id=thread_id,
                    run_id=run.id,
                    tool_outputs=[{
                        "tool_call_id": tool_call.id,
                        "output": json.dumps(output)
                    }]
                )
        
        except Exception as tool_error:
            logging.error(f"Tool call error: {str(tool_error)}")
            # Continue with other tool calls if one fails
            continue


    if attempt == 0:
        attempt = 1
    if time == 0:
        time = 1
    generate_time = math.log10(time * attempt) * time
    return generate_time
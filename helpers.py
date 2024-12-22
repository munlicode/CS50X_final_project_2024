import logging

def overwrite_env_variable(var_name, new_value, env_file=".env"):
    # Step 1: Read the content of the .env file
    with open(env_file, "r") as file:
        lines = file.readlines()

    # Step 2: Look for the variable in the .env file and overwrite it
    var_found = False
    with open(env_file, "w") as file:
        for line in lines:
            # If the line starts with the variable name, overwrite it
            if line.startswith(f"{var_name}="):
                file.write(f"{var_name}={new_value}\n")
                var_found = True
            else:
                # Otherwise, keep the line as is
                file.write(line)

        # If the variable wasn't found, append it to the file
        if not var_found:
            file.write(f"{var_name}={new_value}\n")
    
    logging.info(f"{var_name} has been overwritten with {new_value}.")
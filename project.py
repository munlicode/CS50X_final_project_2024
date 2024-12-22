import sys, cowsay, os, random
from fpdf import FPDF

from data import usage_guide_text, facts, people, options
from assistant import conversation


'''show options'''
def show_options():
    for index, option in enumerate(options):
        yield index, option        

'''show usage'''        
def usage_guide():
    return usage_guide_text

'''math games'''
def games():

    '''calculation game'''
    def calculation_game():
        while True:
            operator = random.choice(['+', '-', '*', '/'])
            x = random.randint(1,100)
            y = random.randint(1,100)
            task = f'{x} {operator} {y}'
            while True:
                try:    
                    answer = input(f'Solve: {task} = ').strip()
                    
                    if answer.lower() in ['answer', 'a']:
                        print(f'Answer: {eval(task)}')
                        break
                    elif float(answer) == float(eval(task)):
                        print('Correct🎉')
                        break

                    else:
                        print('Incorrect❌')

                except EOFError:
                    return print("You're back to games' option menu.")

                except (ValueError, SyntaxError):
                    print('❌Invalid input, please try again.')
            
            if input('Do you want to play again?(y/n) ').strip().lower() in ['y','yes']:
                continue
            break
        
    '''guess person game'''
    def guess_person():
        
        while True:
            try:
                random_person_char = random.choice(list(people.keys()))
                while True:
                    guess = input(f'About person: {random_person_char}\nGuess who is it: ').strip()
                    if guess.lower() == people[random_person_char].lower():
                        print('Correct🎉')
                        break

                    elif guess.lower() in ['answer', 'a']:
                        print(f'Answer: {people[random_person_char]}')
                        break

                    else:
                        print('Incorrect❌')
                    
                
                if input('Do you want to play again?(y/n) ').strip().lower() in ['y', 'yes']:
                    continue
                break
            
            except EOFError:
                return print("You're back to games' option menu.")

    '''games'''
    while True:
        try:
            want = input('Which game do you want to play? (C/G/B) ').strip().lower()
            if want in ['c', 'calculate', 'calculating', 'calculation']:
                calculation_game()

            elif want in ['g', 'guess', 'guessing']:
                guess_person()
            elif want in ['b', 'back']:
                return "You're back to Main Menu."
            else:
                print('❌Invalid game name')
        except EOFError:
                return "You're back to Main Menu."  

'''random fact'''
def random_fact():
    return random.choice(facts)

'''close program'''
def close_program(list_text):
    try:
        text = "\n".join(str(item) for item in list_text)
        answer = input('Do you want to save it? (yes/no) ').strip().lower()
        if answer in ['y', 'yes']:
            while True:
                filetype = input('Enter filetype: ').strip().upper()    
                if not filetype.upper() in ['PDF', 'TXT']:
                    print('❌Invalid filetype! Enter (TXT/PDF).')
                    continue
                while True:
                    name = input('Enter filename: ').strip()
                    filename = name+'.'+filetype.lower()
                    if os.path.exists(filename):
                        print(f'File named "{filename}" already exists.')
                        if input('Do you want to replace data within this file?(Yes/No) ').strip().lower() in ['yes', 'y']:
                            break
                        continue
                    break    
                break
    
                        
            if filetype == 'PDF':
                    try:
                        pdf = FPDF()
                        pdf.add_page()    
                        FONT_PATH = os.getenv('FONT_PATH', r'C:\Users\Nurzhan\my_projects\CS50P_my_project\project\fonts\\')
                        #Adding fonts
                        pdf.add_font("NotoSansMath", "", os.path.join(FONT_PATH,"NotoSansMath-Regular.ttf"))
                        pdf.add_font('notoemoji_medium', '', os.path.join(FONT_PATH,'NotoEmoji-Medium.ttf'))
                        pdf.add_font('notoemoji_light', '', os.path.join(FONT_PATH,'NotoEmoji-Light.ttf'))
                        pdf.add_font('NotoColorEmoji', '', os.path.join(FONT_PATH,'NotoColorEmoji-Regular.ttf'))
                        pdf.add_font('Amatic', '', os.path.join(FONT_PATH, 'AmaticSC-Regular.ttf'))
                        
                        #setting fonts
                        pdf.set_font('NotoSansMath','', 12)
                        pdf.set_fallback_fonts(['notoemoji_medium',
                                                'NotoColorEmoji',
                                                'notoemoji_light',
                                                'Amatic',])
                        
                        pdf.multi_cell(0, 10, text)
                        pdf.output(filename)
                    except UnicodeEncodeError as e:
                        problematic_char = e.object[e.start:e.end]
                        text.replace(problematic_char, '#!')
                        print(f'I have replaced {problematic_char} to "#!"')
            
            elif filetype =='TXT':
                try:
                    with open(filename, 'w', encoding='utf-8') as file:
                        file.write(text)
                except Exception as e:
                    print("Sorry can't save file.\nError:{e}")                    
            
            print(f'Session was saved in a file called "{filename}"✅')    
            
        print('-----------------------------')
        sys.exit(cowsay.cow('Auf Wiedersehen'))

    except EOFError:
        print('Closing current session was cancelled.❎')

'''choices option'''            
def choices(list_text):
    try:
        answer = input('Choose an option(0, 1, 2, 3, 4|keys): ').strip().lower()
        print(f"\n")
        
        if len(answer) == 0:
            return '❌Invalid input! Please choose a valid option.'

        if answer.strip() in ['0', 'use']:
            return usage_guide()
        
        elif answer.strip() in ['1', 'game']:
            return games()
        
        elif answer.strip() in ['2', 'fact']:
            fact = random_fact()
            list_text.append('🔻'+fact+'\n')
            return f'Fact: {fact}'
        
        elif answer.strip() in ['3', 'chat', 'talk']:
            list_text.append('🔻Chat started\n')
            return conversation(list_text)
        
        elif answer.strip() in ['4', 'exit', 'close', 'session']:
            close_program(list_text)
            return "Los geht'es❗"
        else:
            return '❌Invalid input! Please choose a valid option.'

    except EOFError or KeyboardInterrupt:
        print('')
        sys.exit(cowsay.cow('Tschüss'))

def main():
    try:
        list_text = []
        print('Hallo💠')
        while True:
            print('📌Menu:')            
            options = show_options()
            for index, option in options:
                print(f'\n    {index}. {option}')
            print(choices(list_text))
    except EOFError or KeyboardInterrupt:
        print('')
        sys.exit(cowsay.cow('Tschüss'))

if __name__ == "__main__":
    main()
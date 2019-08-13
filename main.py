from selenium import webdriver
from LibSheet import LibSheet
from ExamRobot import ExamRobot
import re

# url to target website
website = 'localhost:8000/college/expaper/edit'
# url to target excel file
excel_url = './lib_sheet.xls'

browser = webdriver.Chrome()
lib_sheet = LibSheet(excel_url)
robot = ExamRobot(lib_sheet, browser)


def show_help():
    print(
        '''Here are all of commands:
  help    Show the introduction of commands
  fill    Autofill the question of target exam 
    --questions     Fill questions
    --captcha       Fill CAPTCHA
    --all           Fill all content of exam
  quit    Quit this program
  search  Search a question
    --radio <question>     Search a radio question
    --checkbox <question>  Search a checkbox question
  reset   Reset setting
    --sheet_path <path>    Reset path of excel file temporarily
    '''
    )


def lines():
    result = re.search(r'(\S+)\s?-{0,2}(\S*)\s?(.*)', input('command> '))
    command = result.group(1)
    option = result.group(2)
    param = result.group(3)
    if command == 'quit':
        print('Program shut down')
        return False
    if command == 'help':
        show_help()
    elif command == 'reset':
        if option == 'sheet_path':
            if lib_sheet.reload(param):
                print('reset successed')
        else:
            print('undefined option')
    elif command == 'search':
        if option == 'radio' or option == 'checkbox':
            if param != '':
                print(lib_sheet.search(0 if option == 'radio' else 1, param))
            else:
                print('param unset')
        else:
            print('undefined option')

    elif command == 'fill':
        if option == 'captcha':
            robot.fill_captcha()
        elif option == 'questions' or option == '':
            robot.fill_questions()
        elif option == 'all':
            robot.fill_questions()
            robot.fill_captcha()
        else:
            print('undefined option')
    else:
        print('undefined command')
    return True


print('program is launching ...')
browser.get(website)
browser.maximize_window()
show_help()
while lines():
    pass
browser.quit()

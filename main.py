from selenium import webdriver
from LibSheet import LibSheet
from ExamRobot import ExamRobot
import re
import configparser as cp

# default config
website_url = 'localhost:8000'
excel_path = './lib_sheet.xls'
print('program is launching ...')

# read user-config from ini 
config = cp.ConfigParser()
config.read('config.ini')
print('loading user-config ...')
website_url = config.get('website','url')
excel_path = config.get('excel','path')
print('website_url',website_url)
print('sheet_path',excel_path)

# load main unit
print('loading main unit ...')
browser = webdriver.Chrome()
lib_sheet = LibSheet(excel_path)
robot = ExamRobot(lib_sheet, browser)


def go(url):
    try:
        browser.get(url)
        return True
    except Exception:
        print('browser get exception')
        print('website_url need protocol part(http/https)')
        return False


def show_help():
    print('''Here are all of commands:
  help    Show the introduction of commands
  fill    Autofill the question of target exam 
    --questions     Fill questions
    --captcha       Fill CAPTCHA
  quit    Quit this program
  search  Search a question
    --radio <question>     Search a radio question
    --checkbox <question>  Search a checkbox question
  reset   Reset setting
    --sheet_path <path>    Reset path of excel file temporarily
    --website_url <url>    Reset url of target website''')

# command lines process
def lines():
    result = re.search(r'(\S+)\s?-{0,2}(\S*)\s?(.*)', input('command> '))
    command, option, param = result.groups()
    if command == 'quit':
        print('Program shut down')
        return False
    if command == 'help':
        show_help()
    elif command == 'reset':
        if option == 'sheet_path':
            if lib_sheet.reload(param):
                config.set('excel','path',param)
                config.write(open('config.ini','r+'))
                print('reset successed')
        elif option == 'website_url':
            if go(param):
                config.set('website','url',param)
                config.write(open('config.ini','r+'))
                print('reset successed')
                browser.get(param)
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
    elif command == 'remove':
        if option == 'blur_cover':
            robot.remove_blur_cover()
        else:
            print('undefined option')
    else:
        print('undefined command')
    return True

# main process launch
go(website_url)
browser.maximize_window()
show_help()
while lines():
    pass
browser.quit()

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import re
import configparser as cp
from util import *
from selenium.webdriver import Proxy

# read user-config from ini
config = cp.ConfigParser()
config.read('data/config.ini')

website_url = config.get('website', 'url')
excel_path = config.get('excel', 'path')
proxy_pool_url = config.get('proxy-pool','url')
print('website_url', website_url)
print('sheet_path', excel_path)

# set proxy
proxy = get_proxy_ip(proxy_pool_url)
settings = {
    "httpProxy": proxy,
    "sslProxy": proxy
}
proxy = Proxy(settings)
cap = DesiredCapabilities.CHROME.copy()
cap['platform'] = "WINDOWS"
cap['version'] = "10"
proxy.add_to_capabilities(cap)
print('proxy_ip',proxy)

# load main unit
browser = webdriver.Chrome(desired_capabilities=cap)
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
    --test          Fill questions for test prupose
  quit    Quit this program
  search  Search a question
    --all <question>
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
                config.set('excel', 'path', param)
                config.write(open('config.ini', 'r+'))
                print('reset successed')
        elif option == 'website_url':
            if go(param):
                config.set('website', 'url', param)
                config.write(open('config.ini', 'r+'))
                print('reset successed')
                browser.get(param)
        else:
            print('undefined option')
    elif command == 'search':
        print(lib_sheet.search(param))
    elif command == 'fill':
        if option == 'captcha':
            robot.fill_captcha()
        elif option == 'questions':
            robot.fill_questions(option)
        elif option == 'all' or option == 'test':
            robot.fill_questions(option)
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


# main process
#  launch
go(website_url)
browser.maximize_window()
show_help()
while lines():
    pass
browser.quit()

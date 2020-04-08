from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from LibSheet import LibSheet
from ExamRobot import ExamRobot
import configparser as cp
import time
import re
import threading

# read user-config from ini
config = cp.ConfigParser()
config.read('config.ini')
website_url = config.get('website', 'url')
excel_path = config.get('excel', 'path')


def process_file(path):
    regex = r'3[\d]1[6,7,8,9]\d{6}'
    with open(path, 'r') as f:
        rawData = f.read()
    dict_list = []
    passwordList = re.split(regex, rawData)
    print(passwordList)
    for i, match in enumerate(re.finditer(regex, rawData)):
        new_dict = {}
        username = match.group(0).strip()
        password = passwordList[i + 1].strip()
        if password == '':
            password = 'nhce111'
        new_dict.setdefault('username', username)
        new_dict.setdefault('password', password)
        dict_list.append(new_dict)
    print(dict_list)
    print(len(dict_list))
    return dict_list


def go(browser, url, username, password):
    browser.get(url)
    browser.implicitly_wait(5)
    browser.execute_script('window.hideMask()')
    browser.maximize_window()
    browser.find_element_by_xpath('//*[@id="root"]/div/div[3]/div/span[1]').click()
    browser.find_element_by_xpath('//*[@id="login-app"]/div/div/form/fieldset[1]/input').send_keys(username)
    browser.find_element_by_name('password').send_keys(password)
    browser.find_element_by_name('password').send_keys(Keys.RETURN)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[4]/div/div[2]/div/div[2]/table/tbody/tr[3]/td[2]').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[1]').click()


def core_process(username, password):
    # load main unit
    browser = webdriver.Chrome()
    lib_sheet = LibSheet(excel_path)
    robot = ExamRobot(lib_sheet, browser)
    try:
        go(browser, website_url, username, password)
        robot.fill_questions()
        robot.fill_captcha()
        browser.find_element_by_xpath('//*[@id="root"]/div/div[4]/div/div[3]/div[2]/p/span[1]').click()
        time.sleep(2)
        browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div[2]/div[1]').click()
        with open('finished.txt', 'a') as f:
            f.write('username: %s, password: %s finished\n' %
                    (consumer_dict.get('username'), consumer_dict.get('password')))
    except:
        with open('unfinished.txt', 'a') as f:
            f.write(consumer_dict.get('username') +
                    ' ' + consumer_dict.get('password') + '\n')
    finally:
        browser.quit()


# main process
#  launch
if __name__ == '__main__':
    for consumer_dict in process_file('customer.txt'):
        threading.Thread(target=core_process, args=(consumer_dict.get('username'),
                                                    consumer_dict.get('password'))).start()

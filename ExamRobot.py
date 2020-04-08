import re
from random import choice, shuffle, randint
import time


class ExamRobot:
    def __init__(self, lib_sheet, browser):
        self.lib_sheet = lib_sheet
        self.browser = browser

    def __choice_option(self, target):
        self.browser.execute_script(
            'arguments[0].click();', target)

    def fill_captcha(self):
        try:
            annotation = self.browser.find_element_by_css_selector(
                'annotation')
            text = annotation.text
            print('annotation', text)
            result = 0
            re_sult = re.search(
                r'(\d+)\\times(\d+)\+(\d+)\-(\d+)=\?', text)
            a, k1, k2, k3 = [int(k) for k in re_sult.groups()]
            result = int(a * k1 + k2 - k3)
            print('result', result)
            inputer = self.browser.find_element_by_css_selector(
                '.captcha-container > div:last-child > input')
            inputer.send_keys(str(result))
        except Exception:
            print('captcha fill exception')

    def fill_questions(self):
        try:
            score = 0
            quizzes = self.browser.find_elements_by_css_selector(
                '.exam-content-quiz')
            for quiz in quizzes:
                time.sleep(randint(10, 20))
                text = quiz.find_element_by_css_selector('p').text
                quiz_text = re.search(r'\d+\.(.+)', text).group(1)
                inputs = quiz.find_elements_by_css_selector('input')
                keys = self.lib_sheet.search(quiz_text)
                for ainput in inputs:
                    if ainput.get_attribute('value') in keys:
                        self.__choice_option(ainput)
                print(text)
                print(keys)
        except Exception as e:
            print(e)
            print('questions fill exception')

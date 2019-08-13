import re


class ExamRobot:
    def __init__(self, lib_sheet, browser):
        self.lib_sheet = lib_sheet
        self.browser = browser

    def fill_captcha(self):
        try:
            annotation = self.browser.find_element_by_css_selector(
                'annotation')
            text = annotation.text
            print('annotation', text)
            result = 0
            if 'int' in text:
                re_sult = re.search(
                    r'\\int_{(\d+)}\^{(\d+)}\((\d+)x\^2\+(\d+)x\+(\d+)\)dx=\?', text)
                a = int(re_sult.group(1))
                b = int(re_sult.group(2))
                k3 = int(re_sult.group(3)) / 3
                k2 = int(re_sult.group(4)) / 2
                k1 = int(re_sult.group(5))
                result = int(k3 * (b ** 3 - a ** 3) + k2 *
                             (b ** 2 - a ** 2) + k1 * (b - a))
            else:
                re_sult = re.search(
                    r'(\d+)\\times(\d+)\+(\d+)\-(\d+)=\?', text)
                a = int(re_sult.group(1))
                k1 = int(re_sult.group(2))
                k2 = int(re_sult.group(3))
                k3 = int(re_sult.group(4))
                result = int(a * k1 + k2 - k3)
            print('result', result)
            inputer = self.browser.find_element_by_css_selector(
                '.captcha-container > div:last-child > input')
            inputer.send_keys(str(result))
        except Exception:
            print('captcha fill exception')

    def fill_questions(self):
        try:
            quizs = self.browser.find_elements_by_css_selector(
                '.exam-content-quiz')
            for quiz in quizs:
                text = quiz.find_element_by_css_selector('div').text
                quiz_text = re.search(r'\d+\.(.+)', text).group(1)
                if '\n' in quiz_text:
                    quiz_text.replace('\n', '')
                inputs = quiz.find_elements_by_css_selector('input')
                quiz_index = 0 if inputs[0].get_attribute(
                    'type') == 'radio' else 1
                keys = self.lib_sheet.search(quiz_index, quiz_text)
                print(text)
                print(keys)
                for ainput in inputs:
                    if ainput.get_attribute('value') in keys:
                        self.browser.execute_script(
                            'arguments[0].click();', ainput)
        except Exception:
            print('questions fill exception')

import re


class ExamRobot:
    def __init__(self, lib_sheet, browser):
        self.lib_sheet = lib_sheet
        self.browser = browser

    def remove_blur_cover(self):
        try:
            cover = self.browser.find_element_by_css_selector(
                '.g-i-w-container')
            self.browser.execute_script(
                'window.WindowBlurDetector.turnOFF;window.WindowBlurDetector.turnON = () => {};')
            print('remove blur_cover succeed')
        except Exception:
            print('remove blur_cover exception')

    def fill_captcha(self):
        try:
            annotation = self.browser.find_element_by_css_selector(
                'annotation')
            text = annotation.text
            result = 0
            if 'int' not in text:
                captcha_box = self.browser.find_element_by_css_selector(
                    '.captcha-container > div:first-child > div')
                self.browser.execute_script(
                    'arguments[0].click();', captcha_box)
                self.fill_captcha()
                return
            print('annotation', text)
            re_sult = re.search(
                r'\\int_{(\d+)}\^{(\d+)}\((\d+)x\^2\+(\d+)x\+(\d+)\)dx=\?', text)
            a, b, k3, k2, k1 = [int(k) for k in re_sult.groups()]
            k3, k2 = k3/3, k2/2
            result = int(k3 * (b ** 3 - a ** 3) + k2 *
                         (b ** 2 - a ** 2) + k1 * (b - a))
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
                text = quiz.find_element_by_css_selector('p').text
                quiz_text = re.search(r'\d+\.(.+)', text).group(1)
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

import xlrd
import re

opts = [
    ['text', 'A', 'B', 'C', 'D', 'key'],
    ['text', 'A', 'B', 'C', 'D', 'E', 'F', 'key']
]


class LibSheet:
    def __init__(self, url):
        self.reload(url)

    def reload(self, url):
        try:
            self.sheets = xlrd.open_workbook(url).sheets()
            self.lib = []
            self.__parse_to_dict()
            return True
        except Exception:
            print('file load exception')
            return False

    def __parse_to_dict(self):
        for k, opt in enumerate(opts):
            sheet = self.sheets[k]
            self.lib.append([])
            for i in range(1, sheet.nrows):
                row_dict = {}
                for j, item in enumerate(sheet.row_values(i)):
                    row_dict[opts[k][j]] = item
                self.lib[k].append(row_dict)

    def __replace(self, text):
        return re.sub(r'[（(）),.，。、\s\t\0\r\n]', '', text)

    def search(self, quiz_index, quiz_text):
        quiz_text = self.__replace(quiz_text)
        for k, item in enumerate(self.lib[quiz_index]):
            if quiz_text == self.__replace(item['text']):
                return item['key']
        return []

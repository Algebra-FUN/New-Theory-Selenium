import xlrd
import re

opt_const = 'ABCDEF'

opts = [
    ['topic', 'A', 'B', 'C', 'D', 'E', 'F', 'ans'],
    ['topic', 'A', 'B', 'C', 'D', 'E', 'F', 'ans']
]


class LibSheet:
    def __init__(self, url):
        self.reload(url)

    def reload(self, url):
        # try:
        self.sheets = xlrd.open_workbook(url).sheets()
        self.lib = []
        self.__parse_to_dict()
        return True
        # except Exception:
        #     print('file load exception')
        #     return False

    def __parse_to_dict(self):
        for k, opt in enumerate(opts):
            sheet = self.sheets[k]
            for i in range(1, sheet.nrows):
                row_dict = {}
                for j, item in enumerate(sheet.row_values(i)):
                    row_dict[opts[k][j]] = item
                self.lib.append(row_dict)

    def __replace(self, text):
        text = re.sub(r'\（.+?\）', '', text)
        text = re.sub(r'[（(）),.，。、\s\t\0\r\n]', '', text)
        return text

    def search(self, quiz_text):
        quiz_text = self.__replace(quiz_text)
        for k, item in enumerate(self.lib):
            topic = self.__replace(item['topic'])
            if quiz_text == topic:
                ans = item['ans']
                try:
                    ans = int(ans)
                    binary = str(bin(ans))[2:][::-1]
                    ans = ''
                    for i, v in enumerate(binary):
                        if v == '1':
                            ans += opt_const[i]
                finally:
                    return ans
        return []

import urllib.request
import re
import time
import os

# Delete QSBK.txt
if os.path.isfile('QSBK.txt'):
    os.remove('QSBK.txt')


class QSBK(object):
    """docstring for QSBK."""

    def __init__(self, baseURL):
        super(QSBK, self).__init__()
        self.baseURL = baseURL
        self.user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36"
        self.headers = {"User-Agent": self.user_agent}

    def get_start(self, start, end):
        for page in range(start, end):
            print("Start : %s" % (page))
            self.get_text(page)
            time.sleep(2)

    def get_item(self, page):
        url = self.baseURL + str(page)
        print("Start page%s: " % (url))
        request = urllib.request.Request(url, headers=self.headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        return content

    def get_text(self, page):
        content = self.get_item(page)
        pattern = re.compile(
            '<div class="author .*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>(.*?)<div class="stats.*?class="number">(.*?)</i>',
            re.S)
        items = re.findall(pattern, content)
        for item in items:
            haveImg = re.search('img', item[2])
            if not haveImg:
                with open('QSBK.txt', 'a') as f:
                    replaceN = re.compile('\n')
                    text = re.sub(replaceN, "", item[1])
                    replaceBR = re.compile('<br/>')
                    text = re.sub(replaceBR, "\n", text)
                    f.write('Author: %s' % (item[0]).strip('\n'))
                    f.write('\nContent: \n%s\n' % (text))
                    f.write('like: %s\n\n' % item[3])
                    f.close()


baseURL = "http://www.qiushibaike.com/hot/page/"
qsbk = QSBK(baseURL)
qsbk.get_start(1, 2)

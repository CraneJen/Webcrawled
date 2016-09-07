import urllib.request
import re
import os

# Delete t.txt
if os.path.isfile('t.txt'):
    os.remove('t.txt')

page = 1

url = "http://www.qiushibaike.com/hot/page/" + str(page)
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
headers = {'User-Agent': user_agent}


try:
    request = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile(
        '<div class="author .*?>.*?<h2>(.*?)</h2>.*?<div class="content">(.*?)</div>(.*?)<div class="stats.*?class="number">(.*?)</i>', re.S)
    items = re.findall(pattern, content)
    for item in items:
        haveImg = re.search('img', item[2])
        if not haveImg:
            with open('t.txt', 'a') as f:
                replaceN = re.compile('\n')
                text = re.sub(replaceN, "", item[1])
                replaceBR = re.compile('<br/>')
                text = re.sub(replaceBR, "\n", text)
                f.write('Author: %s' % (item[0]).strip('\n'))
                f.write('\nContent: \n%s\n' % (text))
                f.write('like: %s\n\n' % item[3])
                f.close()

except urllib.error.URLError as e:
    if hasattr(e, "reason"):
        print(e.reason)

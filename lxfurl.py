import urllib.request
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'Python3TOC.md')

if os.path.isfile(DATA_DIR):
    os.remove(DATA_DIR)
# if os.path.isfile('Python3TOC.txt'):
#     os.remove('Python3TOC.txt')


first = 'wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
url = 'http://www.liaoxuefeng.com/' + first
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

pattern = re.compile(
    '<ul class="uk-nav uk-nav-side" style="margin-right:-15px;">(.*?)</ul>',
    re.S)
patternurl = re.compile(
    '<li id.*?tyle="margin-left:(.*?)em;">.*?<a href=.*?>(.*?)</a>.*?</li>',
    re.S)
urls = re.findall(pattern, content)
path = re.findall(patternurl, urls[0])


def replace_title(x):
    remove_slash = re.compile('/')
    remove_space = re.compile('\s')
    remove_underline = re.compile('_')
    remove_dash = re.compile('---')
    x = re.sub(remove_slash, '', x)
    x = re.sub(remove_space, '-', x)
    x = re.sub(remove_underline, '\_', x)
    x = re.sub(remove_dash, '-', x)
    return x


for url in path:
    listurl = list(url)
    listurl[1] = replace_title(listurl[1])
    if listurl[0] == str(1):
        listurl[1] = '* [%s](/%s.md)' % (listurl[1], listurl[1])
    if listurl[0] == str(2):
        listurl[1] = '    * [%s](/%s.md)' % (listurl[1], listurl[1])
    if listurl[0] == str(3):
        listurl[
            1] = '        * [%s](/%s.md)' % (listurl[1], listurl[1])
    with open(DATA_DIR, 'a') as f:
        f.write(listurl[1] + '\n')
        f.close()

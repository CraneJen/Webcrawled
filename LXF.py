import urllib.request
import re
import time
import os

BADE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LXF(object):
    """docstring for LXF."""

    def __init__(self, baseURL):
        super(LXF, self).__init__()
        self.baseURL = baseURL

    def get_url(self):
        first = 'wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
        url = self.baseURL + first
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        pagecode = response.read().decode('utf-8')
        pattern = re.compile(
            '<ul class="uk-nav uk-nav-side" style="margin-right:-15px;">(.*?)</ul>',
            re.S)
        patternurl = re.compile(
            '<li id.*?>.*?<a href="/(.*?)">.*?</a>.*?</li>', re.S)
        content = re.findall(pattern, pagecode)
        urls = re.findall(patternurl, content[0])
        return urls

    def get_items(self, url):
        url = self.baseURL + url
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')

        pattern = re.compile(
            '<h4>(.*?)</h4>.*?<div class="x-wiki-content">(.*?)</div>', re.S)
        items = re.findall(pattern, content)

        return items

    def replace_content(self, x):
        add_imgpath = re.compile('src="/')
        remove_4space = re.compile('    ')
        x = re.sub(add_imgpath, 'src="http://www.liaoxuefeng.com/', x)
        x = re.sub(remove_4space, '', x)
        return x

    def replace_title(self, x):
        remove_slash = re.compile('/')
        remove_space = re.compile('\s')
        remove_dash = re.compile('---')
        x = re.sub(remove_slash, '', x)
        x = re.sub(remove_space, '-', x)
        x = re.sub(remove_dash, '-', x)
        return x

    def get_content(self):
        for url in self.get_url():
            items = self.get_items(url)
            for item in items:
                content = self.replace_content(item[1])
                title = self.replace_title(item[0])
                md = os.path.join(File_Dir, '%s.md' % (title))
                with open(md, 'a') as f:
                    f.write('## ' + item[0] + '\n')
                    f.write(content + '\n')
                    f.close()
            time.sleep(2)


File_Dir = os.path.join(BADE_DIR, 'Python3Tutorial')
if not os.path.exists(File_Dir):
    os.mkdir(File_Dir)

baseURL = 'http://www.liaoxuefeng.com/'
lxf = LXF(baseURL)
lxf.get_content()

import urllib.request
import re
import time
import os
import shutil


class LXF(object):
    """
    爬取廖雪峰网站Python3的教程内容，保存为MD格式的文件，
    并利用Atom插件markdown-preview-enhanced制成电子书。
    """

    def __init__(self, baseURL):
        super(LXF, self).__init__()
        self.baseURL = baseURL

    def get_url(self):
        first = 'wiki/001434446689867b27157e896e74d51a89c25cc8b43bdb3000'
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
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36'
        }
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        pattern = re.compile(
            '<h4>(.*?)</h4>.*?<div class="x-wiki-content x-main-content">(.*?)</div>',
            re.S)
        items = re.findall(pattern, content)
        return items

    def replace_content(self, content):
        add_imgpath = re.compile('<img src="/files/attachments/(.*?)" alt')
        remove_blankline = re.compile('[\s]*\n')
        remove_tab = re.compile('        <')
        result = re.findall(add_imgpath, content)
        for i in result:
            i = i.replace('/', '')
            rep = '<img src="img/{}" alt'.format(i)
            content = re.sub(add_imgpath, rep, content)
        content = re.sub(remove_blankline, '\n', content)
        content = re.sub(remove_tab, '<', content)
        return content

    def replace_title(self, content):
        remove_slash = re.compile('/')
        remove_space = re.compile('\s')
        remove_dash = re.compile('---')
        content = re.sub(remove_slash, '', content)
        content = re.sub(remove_space, '-', content)
        content = re.sub(remove_dash, '-', content)
        return content

    def get_content(self):
        for url in self.get_url():
            print(url)
            items = self.get_items(url)
            for item in items:
                content = self.replace_content(item[1])
                title = self.replace_title(item[0])
                md = os.path.join(DATA_DIR, '{}.md'.format(title))
                with open(md, 'a') as f:
                    f.write('## ' + title + content)
                    f.close()
            time.sleep(2)


if __name__ == '__main__':
    t1 = time.time()
    print('Start {}'.format(t1))
    baseURL = 'http://www.liaoxuefeng.com/'
    lxf = LXF(baseURL)
    lxf.get_content()
    t2 = time.time()
    print("End {}".format(t2 - t1))

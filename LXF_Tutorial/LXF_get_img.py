import os
import re
from urllib import request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'JavaScriptTutorial')
IMG_DIR = os.path.join(DATA_DIR, 'img')
if not os.path.isdir(IMG_DIR):
    os.mkdir(IMG_DIR)


def get_imgurl(content):
    pattern = re.compile('src="img(.*?)"')
    imgurls = re.findall(pattern, content)
    for imgurl in imgurls:
        video = 'mp4$|swf$'
        if not re.search(video, imgurl):
            imgpath = os.path.join(IMG_DIR, imgurl.replace('/', ''))
            if not imgurl[:4] == 'http':
                imgurl = 'http://www.liaoxuefeng.com/files/attachments' + imgurl
            img = request.urlopen(imgurl).read()
            f = open(imgpath, 'wb')
            f.write(img)
            f.close()


def readitem(itempath):
    f = open(itempath, 'r')
    content = f.read()
    return content
    f.close()


def get_img(DATA_DIR):
    for item in os.listdir(DATA_DIR):
        print(item)
        itempath = os.path.join(DATA_DIR, item)
        if not os.path.isdir(itempath):
            content = readitem(itempath)
            get_imgurl(content)


if __name__ == '__main__':
    get_img(DATA_DIR)

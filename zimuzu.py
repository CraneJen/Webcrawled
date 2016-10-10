import urllib.request
import re
import os

BASE_DIR = os.path.join(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))), 'zimuzu')
if not os.path.exists(BASE_DIR):
    os.mkdir(BASE_DIR)
if os.path.isdir(BASE_DIR):
    for item in os.listdir(BASE_DIR):
        itempath = os.path.join(BASE_DIR, item)
        os.remove(itempath)

url = 'http://www.zimuzu.tv/gresource/list/10733'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'

cookie = 'HPSESSID=733r70i593g3k17mmafmq4feq1; GINFO=uid%3D3545853%26nickname%3Dhwqzqh%26group_id%3D1%26avatar_t%3Dhttp%3A%2F%2Ftu.rrsub.com%2Fftp%2Favatar%2Ff_noavatar_t.gif%26main_group_id%3D0%26common_group_id%3D56; GKEY=38b96d15667280b6e1e8183ce68cef58; CNZZDATA1254180690=1611910511-1475935927-%7C1475935927'

headers = {'User-Agent': user_agent, 'Cookie': cookie}

request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)
codepage = response.read().decode('utf-8')
pattern_title = re.compile('<h2>.*?</span>(.*?)<span')
pattern_ed2k = re.compile('<a href="ed2k:(.*?)" type="ed2k">', re.S)
title = re.findall(pattern_title, codepage)
ed2ks = re.findall(pattern_ed2k, codepage)


CODEPAGE_DIR = os.path.join(BASE_DIR, 'zimuzu.txt')
with open(CODEPAGE_DIR, 'w',) as f:
    f.write(codepage)
    f.close()


for ed2k in ed2ks:
    pattern_1080p = re.compile('1080p.BluRay')
    file_name = title[0] + '1080p.BluRay.txt'
    DATA_DIR = os.path.join(BASE_DIR, file_name)
    if re.search(pattern_1080p, ed2k):
        with open(DATA_DIR, 'a') as f:
            f.write('ed2k:' + ed2k + '\n')
            f.close()

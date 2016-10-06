import urllib.request
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
url = 'http://www.zimuzu.tv/gresource/list/10733'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'

cookie = 'last_item:23885=%E9%92%A2%E9%93%81%E4%BE%A02.%E5%86%85%E5%B0%81%E7%AE%80%E7%B9%81%E8%8B%B1%E5%AD%97%E5%B9%95.Iron.Man.2.2010.1080p.BluRay.x264.DTS-WiKi.mkv; last_item_date:23885=1473094753; last_item:33725=%E6%AF%92%E6%9E%AD.Narcos.S02E09.%E4%B8%AD%E8%8B%B1%E5%AD%97%E5%B9%95.WEBrip.1024x576.mp4; last_item_date:33725=1473095327; mykeywords=a%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22%E5%8D%97%E6%96%B9%E5%85%AC%E5%9B%AD%22%3Bi%3A1%3Bs%3A9%3A%22%E9%92%A2%E9%93%81%E4%BE%A0%22%3B%7D; PHPSESSID=dihskojodjo7o5ea8p94303s44; GINFO=uid%3D3545853%26nickname%3Dhwqzqh%26group_id%3D1%26avatar_t%3Dhttp%3A%2F%2Ftu.rrsub.com%2Fftp%2Favatar%2Ff_noavatar_t.gif%26main_group_id%3D0%26common_group_id%3D56; GKEY=4b85e7c0379827e984d1376dc18e5ea0; CNZZDATA1254180690=1396704648-1470804030-%7C1475779321'

headers = {'User-Agent': user_agent, 'Cookie': cookie}

request = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(request)
codepage = response.read().decode('utf-8')
pattern_title = re.compile('<h2>.*?</span>(.*?)<span')
pattern_ed2k = re.compile('<a href="ed2k:(.*?)" type="ed2k">', re.S)
title = re.findall(pattern_title, codepage)
ed2ks = re.findall(pattern_ed2k, codepage)

# with open('codepage.txt', 'w', encoding='utf8') as f:
#     f.write(codepage)
#     f.close()

for ed2k in ed2ks:
    pattern_1080p = re.compile('1080p.BluRay')
    file_name = title[0] + '1080p.BluRay.txt'
    DATA_DIR = os.path.join(BASE_DIR, file_name)
    if re.search(pattern_1080p, ed2k):
        with open(DATA_DIR, 'a') as f:
            f.write('ed2k:' + ed2k + '\n')
            f.close()

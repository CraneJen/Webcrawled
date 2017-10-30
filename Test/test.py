import os
import re


DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), 'Python3Tutorial')
items = os.listdir(DATA_DIR)
for item in items:
    itempath = os.path.join(DATA_DIR, item)
    if itempath[-2:] == 'md':
        # print(itempath)
        f = open(itempath, 'r')
        content = f.read()
        f.close()
        pattern = re.compile('        <')
        tab = re.findall(pattern, content)
        if tab:
            print(itempath)
            print(tab)
            content = re.sub(pattern, '<', content)
            f = open(itempath, 'w')
            f.write(content)
            f.close()

import urllib.request
import re

url = 'http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431608990315a01b575e2ab041168ff0df194698afac000'
request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

pattern = re.compile(
    '<h4>(.*?)</h4>.*?<div class="x-wiki-content">(.*?)</div>', re.S)
items = re.findall(pattern, content)
print(items)
for item in items:
    add_imgpath = re.compile('src="/')
    content = re.sub(add_imgpath, 'src="http://www.liaoxuefeng.com/', item[1])
    with open('python3.md', 'a') as f:
        f.write('# h3 ' + item[0] + '\n')
        f.write(content)
        f.close()

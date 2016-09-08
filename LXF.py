import urllib.request

baseURL = 'http://www.liaoxuefeng.com/'
first = 'wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000'
url = baseURL + first

request = urllib.request.Request(url)
response = urllib.request.urlopen(request)
content = response.read().decode('utf-8')

with open('python3.md', 'w') as f:
    f.write(content)
    f.close()

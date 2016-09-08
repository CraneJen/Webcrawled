import urllib.request
# import os
response = urllib.request.urlopen("http://www.zhihu.com")

f = open('t.txt', 'w')
f.write(response.read().decode('utf-8'))
f.close()
# print(response.read().decode('utf-8'))

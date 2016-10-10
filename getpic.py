from urllib import request

url = 'http://www.liaoxuefeng.com/files/attachments/0013868176293326466225daa824587bef6bb39c8683c2c000/0'
path = '0013868176293326466225daa824587bef6bb39c8683c2c000/0'
path = path.replace('/', '')
content = request.urlopen(url)
pic = content.read()
fp = open(path, 'wb')
fp.write(pic)
fp.close()

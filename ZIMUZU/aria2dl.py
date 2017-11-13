import xmlrpc.client
import os


def auto_dl():
    SERVER = 'http://192.168.10.1:6800/rpc'
    SECRET = os.environ['token']
    PATH = '/mnt/sda1/aria2'
    with open('dllink.txt', 'r') as f:
        urls = f.readlines()
        for url in urls:
            s = xmlrpc.client.ServerProxy(SERVER)
            s.aria2.addUri('token:{0}'.format(SECRET), [url], {'dir': PATH})


if __name__ == '__main__':
    auto_dl()

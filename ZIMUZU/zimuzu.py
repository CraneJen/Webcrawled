import requests
import os
import sqlite3
from requests.exceptions import RequestException
import re
import xmlrpc.client
import logging
from logging.handlers import RotatingFileHandler


Data_dir = os.path.dirname(os.path.abspath(__file__))

# FORMAT = '[%(levelname)s]: %(asctime)s- %(message)s'
# logging.basicConfig(format=FORMAT, datefmt='%m/%d/%Y %H:%M:%S ', level=logging.INFO)


def getLogger(Data_dir=None, name=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s]: %(asctime)s - %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

    # RotatingFileHandler --> write log to file
    log_dir = os.path.join(Data_dir, '{}.log'.format(name))
    file_handler = RotatingFileHandler(log_dir, maxBytes=5 * 1024 * 1024, backupCount=2, encoding='utf-8', delay=0)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Stream handler --> control log display on screen
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger


def createDB():
    path = os.path.join(Data_dir, 'zimuzu.sqlite3')
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS drama
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        season INT NOT NULL,
        episode INT NOT NULL
        );
        ''')
    cursor.close()
    conn.commit()
    conn.close()


def getCursor(func):
    def wrapper(*args, **kwargs):
        path = os.path.join(Data_dir, 'zimuzu.sqlite3')
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        action = func(cursor, *args, **kwargs)

        conn.commit()
        cursor.close()
        conn.close()
        return action
    return wrapper


@getCursor
def insertData(cursor, name, season, episode):
    cursor.execute("INSERT INTO drama (name,season,episode) \
   VALUES ('{0}',{1},{2});".format(name, season, episode))
    print(cursor.rowcount)


@getCursor
def getByName(cursor, name):
    cursor.execute("SELECT * FROM drama WHERE name='{0}';".format(name))
    value = cursor.fetchall()
    return value


@getCursor
def getAll(cursor):
    cursor.execute("SELECT * FROM drama;")
    return cursor.fetchall()


@getCursor
def updateData(cursor, name, season, episode):
    cursor.execute("UPDATE drama SET season={0}, episode ={1} WHERE name='{2}'".format(season, episode, name))


class ZIMUZU(object):
    """docstring for ZIMUZU"""

    def __init__(self):
        super(ZIMUZU, self).__init__()
        self.url = 'http://www.zimuzu.tv'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/62.0.3202.62 Safari/537.36'
        })
        self.server = 'http://192.168.10.1:6800/rpc'
        self.token = os.environ['token']
        self.path = '/mnt/sda1/aria2'

    def get_auth(self):
        account = os.environ['zmz_account']
        password = os.environ['zmz_password']
        auth = {
            "account": account,
            "password": password
        }
        return auth

    def log_in(self):
        login_url = '{}/User/Login/ajaxLogin'.format(self.url)
        auth = self.get_auth()
        self.session.post(login_url, auth)

    def get_page(self):
        fav_url = '{}/User/Fav?type=ustv'.format(self.url)
        try:
            response = self.session.get(fav_url)
            if response.status_code == 200:
                logger.info('登录成功！')
                return response.text
            else:
                return None
                logger.warning('登录失败，未获取内容！')
        except RequestException as e:
            logger.warning('错误信息{}'.format(e))
            raise e

    def get_items(self):
        content = self.get_page()
        pattern = re.compile(
            ' <div class="user-pop-con">.*?<p>&nbsp;&nbsp;(.*?)</p>.*?<a href="(.*?)" class="corner".*?<div class="clearfix">', re.S)
        items = re.findall(pattern, content)
        return items

    def get_dllink(self):
        items = self.get_items()
        update = False
        for item in items:
            pattern = re.compile('(^\w+)..*?S(\d+)E(\d+).*?', re.S)
            dramas = re.findall(pattern, item[0])
            for drama in dramas:
                name = drama[0]
                season = int(drama[1])
                episode = int(drama[2])
                _drama = getByName(name)
                # new sub
                if _drama == []:
                    insertData(name, season, episode)
                    logger.info('更新剧集《{0}》：S{1}E{2}'.format(name, season, episode))
                    self.aria2_dl(item[1])
                    update = True
                # new season
                elif season > _drama[0][2]:
                    updateData(name, season, episode)
                    logger.info('更新剧集《{0}》：S{1}E{2}'.format(name, season, episode))
                    self.aria2_dl(item[1])
                    update = True
                #  new episode
                elif season == _drama[0][2] and episode > _drama[0][3]:
                    updateData(name, season, episode)
                    logger.info('更新剧集《{0}》：S{1}E{2}'.format(name, season, episode))
                    self.aria2_dl(item[1])
                    update = True

        if update is False:
            logger.info('未更新任何剧集！！！')

    # download the drama by aria2
    def aria2_dl(self, dllink):
        s = xmlrpc.client.ServerProxy(self.server)
        s.aria2.addUri('token:{0}'.format(self.token),
                       [dllink], {'dir': self.path})

    # # write the page to local
    # def write_to_file(self):
    #     content = self.get_page()
    #     with open('result.html', 'w', encoding='utf-8') as f:
    #         f.write(content)
    #         f.close()

    def getCursor(func):
        def __call(*args, **kwargs):
            conn = sqlite3.connect('zimuzu.sqlite3')
            cursor = conn.cursor()
            ret = func(cursor, *args, **kwargs)
            conn.commit()

            cursor.close()
            conn.close()
            return ret
        return __call
        pass


if __name__ == '__main__':
    logger = getLogger(Data_dir=Data_dir, name='zimuzu')
    zimuzu = ZIMUZU()
    zimuzu.log_in()
    zimuzu.get_dllink()

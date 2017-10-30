import requests
import os
import json
from requests.exceptions import RequestException
import re
import xmlrpc.client
import logging
from logging.handlers import RotatingFileHandler

# FORMAT = '[%(levelname)s]: %(asctime)s- %(message)s'
# logging.basicConfig(format=FORMAT, datefmt='%m/%d/%Y %H:%M:%S ', level=logging.INFO)


def getLogger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s]: %(asctime)s- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # RotatingFileHandler
    logger_handler = RotatingFileHandler('{}.log'.format(name), maxBytes=5 * 1024 * 1024, backupCount=2, encoding='utf-8', delay=0)
    logger_handler.setLevel(logging.INFO)
    logger_handler.setFormatter(formatter)

    logger.addHandler(logger_handler)
    return logger


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
        fav_url = '{}/User/Fav'.format(self.url)
        try:
            response = self.session.get(fav_url)
            if response.status_code == 200:
                logger.info('登陆成功！')
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
        with open('episode.json', 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            for item in items:
                patt = re.compile('(^\w+)..*?S(\d+)E(\d+).*?', re.S)
                SE = re.findall(patt, item[0])
                for se in SE:
                    drama = se[0]
                    season = se[1]
                    episode = se[2]
                    if json_data[drama] < episode:
                        logger.info('更新并下载剧集《{0}》/S{1}E{2}'.format(drama, season, episode))
                        self.aria2_dl(item[1])
                        json_data[drama] = episode
                        update = True

        if update is False:
            logger.info('未更新任何剧集！！！')

        with open('episode.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(json_data, indent=4, ensure_ascii=False))
            f.close()

    # download the drama by aria2
    def aria2_dl(self, dllink):
        s = xmlrpc.client.ServerProxy(self.server)
        s.aria2.addUri('token:{0}'.format(self.token),
                       [dllink], {'dir': self.path})


if __name__ == '__main__':
    logger = getLogger('zimuzu')
    zimuzu = ZIMUZU()
    zimuzu.log_in()
    zimuzu.get_dllink()

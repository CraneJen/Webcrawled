import urllib.request
import re
import os
import logging
from logging.handlers import RotatingFileHandler


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


logger = getLogger('ss')


def get_ss():
    # BaseDIR = '/home/cj/Documents/SSDownload/'
    BaseDIR = os.path.dirname(os.path.abspath(__file__))
    baseurl = 'https://github.com'
    url = 'https://github.com/shadowsocks/shadowsocks-android/releases/'
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'
    headers = {'User-Agent': user_agent}

    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        content = response.read().decode('utf-8')
        pattern = re.compile(
            '<ul class="release-downloads">.*?<li>.*?<a href="(.*?)" rel="nofollow">.*?</li>',
            re.S
        )
        items = re.findall(pattern, content)
        # get newest ss apk file
        ss = items[0].split('/')[-1]
        # print(ss)
        # get ss version
        nv = re.findall('v(.*?)/', items[0])[0]
        # set a vserion record
        v_text = os.path.join(BaseDIR, 'v.txt')

        with open(v_text, 'r') as f:
            # get current ss version record
            cv = f.read()
            logger.info('The Downloaded version is {}'.format(cv))
            logger.info('The Newest version is {}'.format(nv))
            # print('The Downloaded version is {}'.format(cv))
            # print('The Newest version is {}'.format(nv))
            if cv < nv:
                with open(v_text, 'w+') as f:
                    f.write(nv)
                command = 'cd ' + BaseDIR + ' && wget ' + baseurl + items[0] + ' && cp ' + ss + ' /var/www/media/ss.apk'
                # print(command)
                logger.info('{}'.format(command))
                print(os.system(command))
            else:
                logger.info('No New ss!!!')
                # print('No New ss!!!')
    except urllib.error.URLError as e:
        logger.warning(e)


if __name__ == '__main__':
    get_ss()

import requests
from requests.exceptions import RequestException
import re
import json
import time
from multiprocessing import Pool


def get_one_page(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except RequestException:
        return None


def parse_one_page(html):
    pattern = re.compile(
        '<dd>.*?board-index.*?">(\d+)</i>.*? title="(.*?)".*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield{
            'index': item[0],
            'title': item[1],
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def process(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


def multiprocess():
    pool = Pool()
    pool.map(process, [i * 10 for i in range(10)])
    pool.close()
    pool.join()


def singleprocess():
    for i in range(10):
        process(i * 10)


def main(mp):
    # clear result.txt
    with open('result.txt', 'w', encoding='utf-8') as f:
        f.write('')
        f.close()
    t1 = time.time()
    print('start {t1}'.format(t1=t1))
    if mp:
        multiprocess()
    else:
        singleprocess()
    t2 = time.time()
    print('end {t2}'.format(t2=t2))


if __name__ == '__main__':
    main(mp=True)

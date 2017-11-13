import requests
import bs4


def get_res(url):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    headers = {'User-Agent': user_agent}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        raise e


def get_moives(res):
    soup = bs4.BeautifulSoup(res, 'html.parser')

    names = []
    targets = soup.find_all("div", class_="hd")
    for target in targets:
        names.append(target.a.span.text)

    ranks = []
    targets = soup.find_all('span', class_="rating_num")
    for target in targets:
        ranks.append('评分： {}'.format(target.text))

    result = []
    length = len(names)
    for i in range(length):
        result.append(names[i] + '    ' + ranks[i] + '\n')
    return result


def get_pages(res):
    soup = bs4.BeautifulSoup(res, 'html.parser')
    pages = soup.find('span', class_='next').previous_sibling.previous_sibling.text
    return int(pages)


def main():
    Base_url = 'https://movie.douban.com/top250'
    res = get_res(Base_url)
    pages = get_pages(res)

    result = []
    for page in range(pages):
        # https://movie.douban.com/top250?start=25&filter=
        url = '{}?start={}&filter='.format(Base_url, str(page * 25))
        res = get_res(url)
        result.extend(get_moives(res))

    with open('moves.txt', 'w', encoding='utf-8') as f:
        for each in result:
            f.write(each + '\n')


if __name__ == '__main__':
    main()

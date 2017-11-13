import requests
import bs4


def so(phone_num):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"
    headers = {'User-Agent': user_agent}
    url = 'https://www.so.com/s?q={}'.format(phone_num)
    res = requests.get(url=url, headers=headers)

    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    targets = soup.find_all('span', class_='mohe-ph-mark')
    if targets:
        for target in targets:
            text = target.text.strip(' \t\n\r')
            return text
    else:
        return "没有不良信息！"

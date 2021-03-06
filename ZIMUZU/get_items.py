import re
import json
import logging


FORMAT = '[%(levelname)s]: %(asctime)s- %(message)s'
logging.basicConfig(format=FORMAT, datefmt='%m/%d/%Y %H:%M:%S ', level=logging.INFO)
logger = logging.getLogger()


def get_items():
    #  get every drama's name season episode  download link from local file
    with open('result.html', 'r', encoding='utf-8') as f:
        content = f.read()
        pattern = re.compile(' <div class="user-pop-con">.*?<p>&nbsp;&nbsp;(.*?)</p>.*?<a href="(.*?)" class="corner".*?<div class="clearfix">', re.S)
        items = re.findall(pattern, content)
        return items


def get_dllink():
    #  if the drama is updated(>episode file's value), get the download link(write to file), update the episode file
    items = get_items()
    update = False
    with open('episode.json', 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        print(json_data)
        for item in items:
            pattern = re.compile('(^\w+)..*?S(\d+)E(\d+).*?', re.S)
            dramas = re.findall(pattern, item[0])
            for drama in dramas:
                title = drama[0]
                season = drama[1]
                episode = drama[2]
                if title not in json_data.keys() or json_data[title].split('/')[1] < episode:
                    logger.info('更新剧集《{0}》/S{1}E{2}'.format(title, season, episode))
                    write_to_file(item[1])
                    json_data[title] = '{}/{}'.format(season, episode)
                    update = True

    if update is False:
        logger.info('未更新任何剧集！！！')

    with open('episode.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(json_data, indent=4, ensure_ascii=False))
        f.close()


def write_to_file(dllink):
    # write the download link to the file
    with open('dllink.txt', 'a', encoding='utf-8') as f:
        f.write(dllink)
        f.close()


if __name__ == '__main__':
    get_dllink()

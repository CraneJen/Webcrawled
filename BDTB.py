import urllib.request
import re

# import time


class BDTB(object):
    """docstring for BDTB."""

    def __init__(self, baseURL, seeLZ):
        super(BDTB, self).__init__()
        self.baseURL = baseURL
        self.seeLZ = '?see_lz=' + str(seeLZ)

    def get_page(self, pageNum):
        try:
            url = self.baseURL + self.seeLZ + '&pn=' + str(pageNum)
            request = urllib.request.Request(url)
            response = urllib.request.urlopen(request)
            # print(response.read().decode('utf-8'))
            return response
            # content = response.read().decode('utf-8')
            # with open('BDTB.txt', 'a') as f:
            #     f.write(content)
            #     f.close()
        except urllib.error.URLError as e:
            if hasattr(e, "reason"):
                print(e.reason)
                return None

    def get_Title(self):
        page = self.get_page(1).read().decode('utf-8')
        # print(page)
        pattern = re.compile('<h3 class="core_title_txt.*?>(.*?)</h3>', re.S)
        result = re.search(pattern, page)
        if result:
            print(result.group(1))
        else:
            return None


baseURL = 'http://tieba.baidu.com/p/3138733512'
bdtb = BDTB(baseURL, 1)
bdtb.get_page(1)
bdtb.get_Title()

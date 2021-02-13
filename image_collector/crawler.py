from bs4 import *
import urllib3
import re

from image_collector.constants import PageName, Tag
from image_collector.image import Image
from image_collector.download import Download
from image_collector.urls import Url
from logs.log import Log

http = urllib3.PoolManager()
prod_url = Url.page(PageName.PROD)
pic_url = Url.page(PageName.PIC)
resp = http.request("GET", prod_url)
soup = BeautifulSoup(resp.data, features="html.parser")  # all contents


class Crawler:
    def __init__(self):
        self.prod_info = soup.findAll(Tag.DIV, {Tag.CLASS: Tag.BOX})
        self.prod_name = soup.findAll(Tag.P, {Tag.CLASS: Tag.MODEL})
        self.prod_image = soup.find_all(Tag.IMG, class_=Tag.PROD_IMG)

    def info(self):
        return self.prod_info
        # prod_price = soup.find_all(Tag.P, {Tag.CLASS: Tag.PRICE})
        # TODO : use for csv later on.


# TODO : move me.
image = Image()
crawler = Crawler()
download = Download(pic_url)
Log.say("pic_url", pic_url)

info = soup.findAll(Tag.DIV, {Tag.CLASS: Tag.BOX})
Log.say("info", info)
Log.say("image list", crawler.prod_image)

# TODO : get gid
detail_url = Url.page(PageName.DETAIL)
Log.say("detail", detail_url)


def extract_last_page():  # Todo : move to pagination
    prod_last_page = soup.find_all(Tag.ANCHOR, {Tag.CLASS: Tag.LAST_PAGE})
    last_page = ""
    for tag in prod_last_page:
        last_page_str = tag.get(Tag.HREF)
        if last_page_str:
            last_page = re.findall("\d+", last_page_str)[-1]

    return int(last_page)  # TODO : Check empty


def extract_prod_link_list(url):
    Log.say("extract product link list", "from %s" % url)

    total_page = extract_last_page()
    Log.say("total_page", total_page)
    link_list = []
    for i in range(total_page):
        li = url + "&page=" + str(i + 1)
        link_list.append(li)

    Log.say("extract complete", link_list)
    return link_list


extract_prod_link_list(prod_url)

img_list = image.get_info_list(crawler.prod_image, crawler.prod_name)
Log.say("img_list", img_list)
# d = download.images(img_list)

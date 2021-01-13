from bs4 import *

import urllib3

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
        self.prod_info = soup.findAll("div", {"class": Tag.BOX})
        self.prod_name = soup.findAll("p", {"class": Tag.MODEL})
        self.prod_image = soup.find_all("img", class_=Tag.IMG)

    def info(self):
        return self.prod_info
        # prod_price = soup.find_all("p", {"class": Tag.PRICE})
        # TODO : use for csv later on.


# TODO : move me.
image = Image()
crawler = Crawler()
download = Download(pic_url)
Log.say("info", crawler.info())

img_list = image.get_info_list(crawler.prod_image, crawler.prod_name)
d = download.images(img_list)

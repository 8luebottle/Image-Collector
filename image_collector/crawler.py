from bs4 import *
import urllib3

from image_collector.constants import PageName, Tag
from image_collector.image import Image
from image_collector.download import Download
from image_collector.urls import Url
from image_collector.spreadsheet import Csv
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

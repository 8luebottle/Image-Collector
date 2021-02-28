from bs4 import *
import urllib3

from image_collector.constants import PageName, Tag
from image_collector.urls import Url

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

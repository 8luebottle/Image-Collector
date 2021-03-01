import urllib3
from bs4 import BeautifulSoup

from confs.config import confs
from image_collector.pagination import PageName
from image_collector.urls import Url
from logs.log import Log

http = urllib3.PoolManager()
Site = confs["site"]


def get_ext(link):
    return link.split(".")[1]


def get_img_path(link):
    for i, l in enumerate(link):
        if l.isdigit():
            return link[i:]


def get_soup(page_name):
    """get soup by page name"""
    resp = http.request("GET", Url.page(page_name))
    return BeautifulSoup(resp.data, features="html.parser")  # all contents


class GID:
    def __init__(self):
        self.prod_url = Url.page(PageName.PROD)
        self.prefix = Site.data_directory() + Site.picture()
        self.suffix = ".jpg"

    def extract_gid_list(self, url_list):
        import itertools
        from image_collector.constants import Tag

        gid_list = []
        name_list = []
        if not url_list:
            url_list = self.prod_url

        for url in url_list:  # TODO : u can enhance us (prd_ids, prd_names)
            Log.say("start to extract gid list", "from %s" % url)
            resp = http.request("GET", url)
            soup = BeautifulSoup(resp.data, features="html.parser")

            product_images = soup.findAll(Tag.DIV, {Tag.CLASS: Tag.PROD_IMG})
            Log.say("total product", len(product_images))

            prd_ids = []
            for tag in product_images:
                src = tag.findChild(Tag.IMG)["src"]
                file_name = src.lstrip(self.prefix)
                gid = file_name.rstrip(self.suffix)
                prd_ids.append(gid)
            Log.say("extract complete product ids(gid)", prd_ids)
            prd_ids = list(filter(None, prd_ids))  # remove empty string form prd_ids
            gid_list.append(prd_ids)

            product_info = soup.find_all(class_=Tag.PROD_NAME)
            prd_names = []
            for tag in product_info:
                name = tag.get_text()
                prd_names.append(name)
            Log.say("extract complete product names", prd_names)
            prd_names = list(filter(None, prd_names))
            name_list.append(prd_names)

        flatten_gids = list(itertools.chain(*gid_list))  # flatten two-dimensional list
        flatten_names = list(itertools.chain(*name_list))
        return flatten_gids, flatten_names

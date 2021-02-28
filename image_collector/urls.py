from urllib.parse import urlunparse, ParseResult

from confs.config import confs
from image_collector.constants import PageName


Site = confs["site"]


class Url:
    @staticmethod
    def page(page_name=""):
        directory = Site.sys_directory()
        path = ""
        query = ""
        if page_name == PageName.PROD:
            sub_dir = Site.product()
            path = directory + sub_dir
            query = "cal1=1"
        if page_name == PageName.MANUAL:
            sub_dir = Site.manual()
            path = directory + sub_dir
            query = "pageid=36"
        if page_name == PageName.PIC:
            path = Site.data_directory() + Site.picture()
        if page_name == PageName.DETAIL:
            sub_dir = Site.product_detail()
            path = directory + sub_dir
            query = "gid="

        url = ParseResult(
            scheme=Site.scheme(),
            netloc=Site.domain(),
            path=path,
            params="",
            query=query,
            fragment="",
        )
        return urlunparse(url)

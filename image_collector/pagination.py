import re

from image_collector.constants import PageName, Tag
from image_collector.utils import get_soup
from logs.log import Log

soup = get_soup(PageName.PROD)


class Pagination:
    @staticmethod
    def extract_last_page():
        prod_last_page = soup.find_all(Tag.ANCHOR, {Tag.CLASS: Tag.LAST_PAGE})
        last_page = ""
        for tag in prod_last_page:
            last_page_str = tag.get(Tag.HREF)
            if last_page_str:
                last_page = re.findall("\d+", last_page_str)[-1]

        return int(last_page)  # TODO : Check empty

    @staticmethod
    def extract_prod_link_list(url):
        Log.say("extract product link list", "from %s" % url)

        total_page = Pagination.extract_last_page()
        Log.say("total_page", total_page)
        link_list = []
        for i in range(total_page):
            li = url + "&page=" + str(i + 1)
            link_list.append(li)

        Log.say("extract complete", link_list)
        return link_list

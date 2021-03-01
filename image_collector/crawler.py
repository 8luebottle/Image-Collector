from image_collector.constants import PageName, Tag
from image_collector.urls import PageUrl
from image_collector.utils import get_soup

pic_url = PageUrl.pictures()
soup = get_soup(PageName.PROD)


class Crawler:
    def __init__(self):
        self.prod_info = soup.findAll(Tag.DIV, {Tag.CLASS: Tag.BOX})
        self.prod_name = soup.findAll(Tag.P, {Tag.CLASS: Tag.PROD_NAME})
        self.prod_image = soup.find_all(
            Tag.IMG, class_=Tag.PROD_IMG
        )  # TODO : update me
        self.prod_price = soup.findAll(Tag.P, {Tag.CLASS: Tag.PRICE})

    def prod_info(self):
        return self.prod_info

    def prod_name(self):
        return self.prod_name

    def prod_image(self):
        return self.prod_image

    def prod_price(self):
        return self.prod_price

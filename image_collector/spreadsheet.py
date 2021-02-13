# Convert HTML product info to CSV
from bs4 import BeautifulSoup
import urllib3

from confs.config import confs
from image_collector.constants import PageName, Tag
from image_collector.urls import Url
from logs.log import Log


http = urllib3.PoolManager()
Site = confs["site"]


class Csv:
    def __init__(self):
        self.prod_url = Url.page(PageName.PROD)
        self.prod_detail_url = Url.page(PageName.DETAIL)
        self.want = ["가격", "내부 사이즈", "외부 사이즈", "무게"]
        self.prefix = Site.data_directory() + Site.picture()
        self.suffix = ".jpg"

    def extract_gid_list(self):
        Log.say("extract gid list", "from %s" % self.prod_url)
        resp = http.request("GET", self.prod_url)
        soup = BeautifulSoup(resp.data, features="html.parser")  # all contents
        products = soup.findAll(Tag.DIV, {Tag.CLASS: Tag.PROD_IMG})
        Log.say("total product", len(products))

        gid_list = []
        for tag in products:
            src = tag.findChild(Tag.IMG)["src"]
            file_name = src.lstrip(self.prefix)
            gid = file_name.rstrip(self.suffix)
            gid_list.append(gid)

        Log.say("extract complete", gid_list)
        return gid_list

    def get_prd_detail(self, gid_list):
        Log.say("get product detail", "from %s" % self.prod_detail_url)

        title_rows = [""]
        data_rows = []
        for gid in gid_list:
            resp = http.request("GET", self.prod_detail_url + gid)
            soup = BeautifulSoup(resp.data, features="html.parser")

            info = soup.findAll(Tag.DIV, {Tag.CLASS: Tag.PROD_INFO})
            table = soup.find(Tag.TABLE)
            rows = table.findAll(Tag.TABLE_ROW)

            for tag in info:
                product_name = tag.find(
                    Tag.P, attrs={Tag.CLASS: Tag.PROD_NAME}
                ).text.strip()
                title_rows.append(product_name)

            for row in rows:
                cell = []
                headers = row.findAll(Tag.TABLE_HEADER)
                columns = row.findAll(Tag.TABLE_DATA)
                for header in headers:
                    th = header.text.strip()
                    cell.append(th)

                for column in columns:
                    td = column.text.strip()
                    cell.append(td)

                data_rows.append(cell)

        return title_rows, data_rows

    def normalize_data(self, data_array, title_array):
        key, value = (0, 1)
        nor_list = list()  # normalized list
        for data in data_array:
            if data[key] in self.want:
                nor_dict = dict()
                if data[value]:
                    nor_dict[data[key]] = data[value]
                nor_list.append(nor_dict)

        fin_dict = dict()  # finalized list
        for i, title in enumerate(title_array):
            if title:
                fin_dict[title] = nor_list[i: i + len(self.want)]

        return fin_dict

    # TODO : CSV Generator


c = Csv()
glist = c.extract_gid_list()
titles, csv_data = c.get_prd_detail(glist)

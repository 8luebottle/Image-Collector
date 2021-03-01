# Convert HTML product info to CSV
import csv
import os
import urllib3
from bs4 import BeautifulSoup

from image_collector.constants import File, Folder, Tag
from image_collector.pagination import Pagination
from image_collector.urls import PageUrl
from image_collector.utils import GID
from logs.log import Log


http = urllib3.PoolManager()


class Csv:
    def __init__(self):
        self.prod_detail_url = PageUrl.details()
        self.want = ["가격", "내부 사이즈", "외부 사이즈", "무게"]
        self.header = ["모델"] + self.want

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

        title_rows[:] = [ele for ele in title_rows if ele]  # remove empty string
        return title_rows, data_rows

    def normalize_data(self, data_array, title_array):
        Log.say("data normalization")

        key, value = (0, 1)
        nor_list = list()  # normalized list
        for data in data_array:  # generate model name list
            if data[key] in self.want:
                nor_dict = dict()
                if data[value]:
                    nor_dict[data[key]] = data[value]
                nor_list.append(nor_dict)

        finalized_list = []
        for i, title in enumerate(title_array):  # generate detail info of a model
            temp_dict = dict()
            finalized_list.append(title)
            temp = nor_list[i : i + len(self.want)]
            for v in temp:
                temp_dict.update(v)

            finalized_list.append(temp_dict)
        Log.say("finalized list", finalized_list)
        return finalized_list

    def generate_2d_list(self, data_list, title_list):
        Log.say("generate 2d list")

        two_d_list = list()
        for data in data_list:
            if type(data) == dict:
                columns = self.header
                temp_list = ["", "", "", "", ""]
                for k, v in data.items():
                    ind = columns.index(k)
                    temp_list[ind] = v
                two_d_list.append(temp_list)

        for i, title in enumerate(title_list):
            two_d_list[i][0] = title

        return two_d_list

    def create_csv_file(self, two_d_list):
        Log.say("create CSV file")
        file_path = Folder.PROD_PATH + File.CSV
        file_path = os.path.join(os.path.dirname(__file__), file_path)
        if not os.path.exists(Folder.PROD_NAME):
            Log.say("Create new folder")
            os.mkdir(Folder.PROD_NAME)

        Log.say("open csv file", File.CSV)
        file = open(file_path, "w+", newline="")

        Log.say("start to write data")
        writer = csv.writer(file, delimiter=",")
        writer.writerow(self.header)
        writer.writerows(two_d_list)
        Log.say("successfully write data to CSV")

        file.close()
        Log.say("save and close", File.CSV)


def generate_csv():
    gid = GID()
    c = Csv()

    url_list = Pagination.extract_prod_link_list(PageUrl.products())
    gid_list, prd_names = gid.extract_gid_list(url_list=url_list)  # skip prd_names
    titles, csv_data = c.get_prd_detail(gid_list)
    normalized_list = c.normalize_data(csv_data, titles)
    rows = c.generate_2d_list(normalized_list, titles)

    c.create_csv_file(rows)

import os
import urllib.request

from image_collector.constants import Folder
from image_collector.pagination import Pagination
from image_collector.urls import PageUrl
from image_collector.utils import GID
from logs.log import Log

img_dir = Folder.IMG_PATH
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

pic_url = PageUrl.pictures()
prod_url = PageUrl.products()


class Download:
    @staticmethod
    def images(prd_ids, prd_names):
        for i, img_info in enumerate(prd_ids):
            url = pic_url + img_info + ".jpg"
            Log.say("download images #{} :".format(i), url)
            urllib.request.urlretrieve(url, filename=prd_names[i] + ".jpg")


# TODO : FIX FileNotFoundError:
#        [Errno 2] No such file or directory: (few image)
def download_images():
    download = Download()
    gid = GID()

    url_list = Pagination.extract_prod_link_list(prod_url)
    gid_list, name_list = gid.extract_gid_list(url_list=url_list)
    download.images(gid_list, name_list)

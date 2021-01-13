import os
import urllib.request

from logs.log import Log


# TODO : move me to the nice place.
dir = "../images"
if not os.path.exists(dir):
    os.makedirs(dir)


class Download:
    def __init__(self, page_url):
        self.page = page_url

    def images(self, img_list):
        for i, img_info in enumerate(img_list):
            url = self.page + img_info["file_path"]
            Log.say("download images #{} :".format(i), url)
            urllib.request.urlretrieve(
                url, filename=img_info["name"] + "." + img_info["ext"]
            )

from image_collector.utils import get_ext, get_img_path


class Image:
    def __init__(self):
        self.list = list()

    def get_info_list(self, prod_img, prod_name):
        if len(prod_name) == len(prod_img):
            for n, l in zip(prod_name, prod_img):
                info = dict()
                name = n.string
                link = l["src"]

                info["name"] = name
                info["file_path"] = get_img_path(link)
                info["ext"] = get_ext(link)

                self.list.append(info)

        return self.list

def get_ext(link):
    return link.split(".")[1]


def get_img_path(link):
    for i, l in enumerate(link):
        if l.isdigit():
            return link[i:]

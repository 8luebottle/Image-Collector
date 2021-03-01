from pathlib import Path

parent = str(Path(__file__).absolute().parent)


class File:
    CSV = "product_info.csv"


class Folder:
    PROD_NAME = "products"
    PROD_PATH = parent + "/" + PROD_NAME
    IMG_NAME = "images"
    IMG_PATH = parent + "/" + IMG_NAME


class PageName:
    DETAIL = "detail"
    HOME = "home"
    MANUAL = "manual"
    PROD = "product"
    PIC = "picture"


class Tag:
    from confs.config import confs

    ClassTag = confs["tag"]

    # Customized tags
    BOX = ClassTag.box()
    MODEL = ClassTag.model()
    PROD_IMG = ClassTag.product_img()
    PROD_INFO = ClassTag.product_info()
    PROD_NAME = ClassTag.product_name()
    PRICE = ClassTag.price()
    LAST_PAGE = ClassTag.last_page()

    # HTML tags
    ANCHOR = "a"
    CLASS = "class"
    DIV = "div"
    HREF = "href"
    IMG = "img"
    P = "p"
    TABLE = "table"
    TABLE_DATA = "td"
    TABLE_HEADER = "th"
    TABLE_ROW = "tr"

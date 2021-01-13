class PageName:
    HOME = "home"
    PROD = "product"
    MANUAL = "manual"
    PIC = "picture"


class Tag:
    from confs.config import confs

    ClassTag = confs["tag"]

    BOX = ClassTag.box()
    IMG = ClassTag.img()
    MODEL = ClassTag.model()
    PRICE = ClassTag.price()
    P = "p"
    DIV = "div"

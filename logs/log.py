from icecream import ic


def timestamped_printer():
    import datetime

    n = datetime.datetime.utcnow()
    return " %s | " % str(n)[:19]


class Log:
    """crawler log"""

    ic.configureOutput(prefix=timestamped_printer())

    @staticmethod
    def say(about="", detail=""):
        ic(about, detail)

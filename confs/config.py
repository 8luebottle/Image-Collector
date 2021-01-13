import yaml

from pathlib import Path

p = Path(__file__).resolve()
config_path = p.parent / "config.yaml"

with config_path.open() as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


class Site:
    def __init__(self):
        self._target = config["target"]
        self._sys_dir = self._target["sys_dir"]
        self._data_dir = self._target["data_dir"]

    def scheme(self):
        return self._target["scheme"]

    def domain(self):
        return self._target["domain"]

    def sys_directory(self):
        return self._sys_dir["name"]

    def product(self):
        return self._sys_dir["product"]

    def manual(self):
        return self._sys_dir["manual"]

    def data_directory(self):
        return self._data_dir["name"]

    def picture(self):
        return self._data_dir["picture"]


class Tag:
    def __init__(self):
        self._tag = config["tag"]

    def box(self):
        return self._tag["box"]

    def img(self):
        return self._tag["img"]

    def model(self):
        return self._tag["model"]

    def price(self):
        return self._tag["price"]


confs = {
    "site": Site(),
    "tag": Tag()
}

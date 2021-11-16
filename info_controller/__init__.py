import pathlib
import re
import yandex


class Music:
    def __init__(self, url: str):
        self.id = ""
        self.title = ""
        self.artists = ""
        self.file = None

    def __str__(self):
        return f"{self.title} - {self.artists}"

    def load(self) -> pathlib.Path:
        pass

def get_song(url: str):
    if re.match(r"(https?://)?music\.yandex\.../album/.*/track/.*", url):
        return yandex.Music(url)
    elif url.find(""):
        pass

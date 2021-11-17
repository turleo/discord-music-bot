import pathlib


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
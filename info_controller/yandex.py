import os
import pathlib

from yandex_music import Client
from yandex_music.exceptions import BadRequest
from yandex_music.track.track import Track
from .base import Music as Original

user = os.environ.get("yandex_user")
password = os.environ.get("yandex_password")
if user is not None and password is not None:
    try:
        client = Client.from_credentials(user, password)
    except BadRequest:
        client = Client()
else:
    client = Client()
temp_dir = pathlib.Path(os.environ.get("temp_path", "."))


class Track(Original):
    def __init__(self, url: str):
        super().__init__(url)
        url = url.split("/")
        music_id = f"{url[6]}:{url[4]}"
        track = client.tracks([music_id])
        self.track: Track = track[0]
        self.id = f"ya.{self.track.id}"
        self.title = self.track.title
        self.artists = ', '.join([i.name for i in self.track.artists])
        self.version = "(" + self.track.version + ")" if self.track.version else ""
        self.file = None
        self.load()

    def __str__(self):
        return f"{self.title} - {self.artists} {self.version}"

    def load(self):
        file_path = temp_dir / f"{self.id}.mp3"
        if not file_path.exists():
            info = self.track.get_download_info()[0]
            self.track.download(str(file_path), info.codec, info.bitrate_in_kbps)
        self.file = file_path
        return self.file

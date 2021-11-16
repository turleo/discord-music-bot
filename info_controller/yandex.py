import os
import pathlib

from yandex_music import Client
from yandex_music.track.track import Track

from . import Music as Original

client = Client()
temp_dir = pathlib.Path(os.environ.get("temp_path", "."))

class Music(Original):
    def __init__(self, url: str):
        url = url.split("/")
        music_id = f"{url[6]}:{url[4]}"
        track = client.tracks([music_id])
        self.track: Track = track[0]
        self.id = f"ya.{self.track.id}"
        self.title = self.track.title
        self.artists = ', '.join([i.name for i in self.track.artists])
        self.version = "(" + self.track.version + ")" if self.track.version else ""
        self.file = None

    def __str__(self):
        return f"{self.title} - {self.artists} {self.version}"

    def load(self):
        file_path = temp_dir / f"{self.id}.mp3"
        if not file_path.exists():
            info = self.track.get_download_info()[0]
            self.track.download(str(file_path), info.codec, info.bitrate_in_kbps)
        self.file = file_path
        return self.file

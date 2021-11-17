import pathlib, os
from .base import Music as Original
from pytube import YouTube, Stream


temp_dir = pathlib.Path(os.environ.get("temp_path", "."))

class Video(Original):
    def __init__(self, url: str):
        super().__init__(url)
        self.url = url
        self.yt = YouTube(url)
        self.title = self.yt.title
        self.artists = self.yt.author
        self.file = None

    def load(self) -> pathlib.Path:
        path = temp_dir / f"u{self.yt.video_id}.mp3"
        if not path.exists():
            stream: Stream = \
                sorted(self.yt.streams.filter(only_audio=True), key=lambda x: int(x.abr.replace("kbps", "")))[0]
            stream.download(str(path.parent), path.name)
        self.file = path
        return path


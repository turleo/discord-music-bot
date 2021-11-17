from .base import Music
import re
from .yandex import Track as YandexMusic
from .youtube import Video as Youtube


def get_song(url: str) -> Music:
    if re.match(r"(https?://)?music\.yandex\.../album/.*/track/.*", url):
        return YandexMusic(url)
    elif re.match(r"(https?://)?(www.)?youtu\.?be(.com)?/(watch)?([?&])?(v=)?.*", url):
        return Youtube(url)
    return None

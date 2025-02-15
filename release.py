#!/usr/bin/env python3
import argparse
import logging
import os
import re
import shutil
from html.parser import HTMLParser

from constants import FEEDS, S3_BUCKET, S3_ENDPOINT
from functions import logger
from functions.gen_cover import (
    gen_cover,
    prepare_rss_cover,
    prepare_video_cover,
    prepare_vk_cover,
)
from functions.publish_post import publish_post
from functions.s3 import copy_file

screen_width, _ = shutil.get_terminal_size()
screen_width -= 1


class HTMLFilter(HTMLParser):
    text = ""

    def handle_data(self, data):
        self.text += data


def excerpt(text):
    f = HTMLFilter()
    f.feed(text)
    return f.text


def format_output(text: str, value: str) -> str:
    return f'{text + ":": <20}{value}\n'


class Podcast:
    def __init__(self, title, description, mp3, img=None, date=None):
        self.title = title
        self.description = description
        self.excerpt = excerpt(self.description)
        self.feed = self.get_feed()

        self.body = self.site_body

        self.episode_number = self.get_number()

        self.filename = f"{self.feed}-V{self.episode_number}"

        self.mp3 = mp3
        self.mp3_filename = f"{self.filename}.mp3"

        if date:
            self.date = date

        if img:
            self.img = img
        else:
            self.img = f"img/defaults/{self.feed}_img.png"

        if not os.path.exists(self.img):
            raise ValueError(f"Файл {self.img} не существует")

        if self.feed == "donasdoshlo":
            self.img = gen_cover(self)

        img_extension = img.split(".")[-1]
        self.img_filename = f"{self.filename}.{img_extension}"

    def get_feed(self) -> str:
        first_word = self.title.split()[0]
        return FEEDS[first_word] if FEEDS.get(first_word) else "other"

    def get_number(self) -> str:
        if "Внеплановый" in self.title:
            return "Внеплановый Новогодний"

        if self.feed == "donasdoshlo":
            regexp = r"\S+ *№ ?(?P<number>s\d+e\d+)\..*"
        else:
            regexp = r"\S+ *№ ?(?P<number>\d+)\..*"
        result = re.search(regexp, self.title)
        return result.group("number")

    def create_covers(self):
        self.cover = gen_cover(self)
        self.cover_filename = self.cover.split("/")[-1]

        if self.feed != "donasdoshlo":
            self.rss_cover = prepare_rss_cover(self)
            self.vk_cover = prepare_vk_cover(self)
        else:
            self.img = self.cover
            self.rss_cover = prepare_rss_cover(self)
            self.vk_cover = prepare_vk_cover(self)
            self.video_cover = prepare_video_cover(self)

        self.rss_cover_filename = self.rss_cover.split("/")[-1]
        self.vk_cover_filename = self.vk_cover.split("/")[-1]

    def mp3_upload(self):
        file_path = f"podcasts/{self.feed}/{self.mp3_filename}"
        copy_file(self.mp3, file_path, "audio/mpeg")
        self.podtrac_url = f"{S3_ENDPOINT}/{S3_BUCKET}/{file_path}"

    def img_upload(self):
        file_path = f"images/podcasts/{self.feed}/{self.img_filename}"
        copy_file(self.img, file_path, "image/png")
        self.img_url = f"{S3_ENDPOINT}/{S3_BUCKET}/{file_path}"

    def cover_upload(self):
        file_path = f"images/podcasts/{self.feed}/{self.cover_filename}"
        copy_file(self.cover, file_path, "image/png")
        self.cover_url = f"{S3_ENDPOINT}/{S3_BUCKET}/{file_path}"

    def rss_cover_upload(self):
        file_path = f"images/podcasts/{self.feed}/{self.rss_cover_filename}"
        copy_file(self.rss_cover, file_path, "image/png")
        self.rss_cover_url = f"{S3_ENDPOINT}/{S3_BUCKET}/{file_path}"

    def publish_to_site(self):
        self.post_url = publish_post(self, args.announce)
        self.description += f"\n{self.post_url}"

    def render(self):
        self.mp4 = render_video(self, args.need_render)

    def yt_upload(self):
        # self.yt_id = upload_video(self)
        # update_playlist(self)
        self.yt_url = f"https://www.youtube.com/watch?v={self.yt_id}"

    @property
    def nice_view(self) -> str:

        output = "=" * screen_width
        output += format_output("\ntitle", self.title)
        output += format_output("feed", self.feed)
        output += format_output("original_mp3", self.mp3)
        output += format_output("mp3_file", self.mp3_filename)
        if hasattr(self, "podtrac_url"):
            output += format_output("podcast url", self.podtrac_url)

        if hasattr(self, "img"):
            output += format_output("original_img", self.img)

        if hasattr(self, "img_url"):
            output += format_output("img url", self.img_url)

        if hasattr(self, "cover_url"):
            output += format_output("cover url", self.cover_url)

        if hasattr(self, "rss_cover_url"):
            output += format_output("rss_cover url", self.rss_cover_url)

        if hasattr(self, "vk_cover"):
            output += format_output("vk_cover_filename", self.vk_cover_filename)

        if hasattr(self, "mp4"):
            output += format_output("mp4", self.mp4)

        if hasattr(self, "yt_id"):
            output += format_output("youtube id", self.yt_id)
            output += format_output("youtube url", self.yt_url)

        if hasattr(self, "post_url"):
            output += format_output("post_url", self.post_url)

        output += "=" * screen_width

        return output

    @property
    def yt_body(self) -> str:

        f = HTMLFilter()
        f.feed(self.description)

        return (
            f.text.replace(">", "-").replace("<", "-")
            + """


        ------------------------------------------------------------
        Пишите нам: info@linkmeup.ru
        Канал в телеграме: https://t.me/linkmeup_podcast​
        Подкаст доступен в iTunes, Google Подкастах, Яндекс Музыке, Castbox
        Сообщество в вк: https://vk.com/linkmeup​
        Группа в фб: https://www.facebook.com/linkmeup.sdsm​
        Пообщаться в общих чатах в тг:
        - https://t.me/linkmeup_chat
        - https://t.me/linkmeup_sysadm_chat​

        Поддержите проект:
        - https://www.patreon.com/linkmeup
        - https://sponsr.ru/linkmeup/
        - https://boosty.to/linkmeup
        ------------------------------------------------------------
    """
        )

    @property
    def site_body(self) -> str:

        if self.feed != "donasdoshlo":
            body = """

<blockquote>
    <h5>Оставайтесь на связи</h5>
    Пишите нам: <a href="mailto:info@linkmeup.ru" rel="nofollow">info@linkmeup.ru</a><br />
    Канал в телеграме: <a href="https://t.me/linkmeup_podcast">t.me/linkmeup_podcast</a><br />
    Канал на youtube: <a href="https://youtube.com/c/linkmeup-podcast">youtube.com/c/linkmeup-podcast</a><br />
    Подкаст доступен в <a href="https://itunes.apple.com/ru/podcast/linkmeup.-pervyj-podkast-dla/id1065445951?mt=2">iTunes</a>, <a href="https://podcasts.google.com/feed/aHR0cHM6Ly9saW5rbWV1cC5ydS9yc3MvcG9kY2FzdHM">Google Подкастах</a>, <a href="https://music.yandex.ru/album/7060168">Яндекс Музыке</a>, <a href="https://castbox.fm/channel/linkmeup.-Подкаст-про-IT-и-про-людей-id1173801?country=ru">Castbox</a><br />
    Сообщество в вк: <a href="https://vk.com/linkmeup">vk.com/linkmeup</a><br />
    Группа в фб: <a href="https://www.facebook.com/linkmeup.sdsm/">www.facebook.com/linkmeup.sdsm</a><br />
    Добавить <a href="https://linkmeup.ru/rss/podcasts">RSS</a> в подкаст-плеер.<br />
    Пообщаться в общем чате в тг: <a href="https://t.me/linkmeup_chat">https://t.me/linkmeup_chat</a><br />
    <br />

    <b>Поддержите проект:</b><br />

    <a href="https://www.patreon.com/linkmeup?ty=h" target="_blank" rel="noopener"><img title="Поддержать нас на Patreon" src="https://s3.linkmeup.ru/linkmeup/images/patreon.jpg" width="300" align="middle" /></a>

    <a href="https://sponsr.ru/linkmeup/" target="_blank" rel="noopener"><img title="Поддержать нас на Sponsr" src="https://s3.linkmeup.ru/linkmeup/images/sponsr.png" width="300" align="middle" /></a>

    <a href="https://boosty.to/linkmeup" target="_blank" rel="noopener"><img title="Поддержать нас на boosty" src="https://s3.linkmeup.ru/linkmeup/images/boosty.png" width="300" align="middle" /></a>
</blockquote>
"""

        else:
            body = """

<blockquote>
    <h5>Оставайтесь на связи</h5>
    Кто мы такие: <a href="https://linkmeup.ru/about/">"https://linkmeup.ru/about/</a><br/>
    Пишите нам: <a href="mailto:info@linkmeup.ru" rel="nofollow">info@linkmeup.ru</a><br/>
    Канал в телеграме: <a href="https://t.me/donasdoshlo">https://t.me/donasdoshlo</a>. Приходите обсуждать и предлагать.<br/>
    Плейлист подкаста на <a href="https://www.youtube.com/playlist?list=PLHN9m7XN8U8Enp72zrhlYd3o0pcifFpox">Youtube</a><br/>

    <br />

    <b>Поддержите проект:</b><br />

    <a href="https://www.patreon.com/linkmeup?ty=h" target="_blank" rel="noopener"><img title="Поддержать нас на Patreon" src="https://s3.linkmeup.ru/linkmeup/images/patreon.jpg" width="300" align="middle" /></a>

    <a href="https://sponsr.ru/linkmeup/" target="_blank" rel="noopener"><img title="Поддержать нас на Sponsr" src="https://s3.linkmeup.ru/linkmeup/images/sponsr.png" width="300" align="middle" /></a>

    <a href="https://boosty.to/linkmeup" target="_blank" rel="noopener"><img title="Поддержать нас на boosty" src="https://s3.linkmeup.ru/linkmeup/images/boosty.png" width="300" align="middle" /></a>
</blockquote>
"""

        return self.description + body


def main():

    # Initialize logger
    logger.init_logging(0)
    log = logging.getLogger(__name__)

    with open(args.description_file, "r") as f:
        description = f.read()

    podcast = Podcast(args.title, description, args.mp3, args.img, args.announce)
    print(podcast.feed)

    log.info(podcast.yt_body)

    # Generate podcast covers
    log.delimiter("=" * screen_width)
    log.topic("Рисуем обложки")
    podcast.create_covers()
    log.info("  Готово.")

    # return #!!!
    # Upload covers to file-hosting
    log.delimiter("-" * screen_width)
    log.topic("Загружаем изображение выпуска на s3")
    podcast.img_upload()
    log.info("\n  Готово.")

    log.delimiter("-" * screen_width)
    log.topic("Загружаем обложку выпуска на s3")
    podcast.cover_upload()
    log.info("\n  Готово.")

    log.delimiter("-" * screen_width)
    log.topic("Загружаем обложку выпуска для RSS на s3")
    podcast.rss_cover_upload()
    log.info("\n  Готово.")

    if not args.announce:

        # Upload mp3 to file-hosting
        log.delimiter("-" * screen_width)
        log.topic("Загружаем mp3 на s3")
        podcast.mp3_upload()
        log.info("\n  Готово.")

    # Post podcast to site
    log.delimiter("-" * screen_width)
    log.topic("Публикуем пост на сайте")
    podcast.publish_to_site()
    log.info("\n  Готово.")

    log.info(podcast.nice_view)


parser = argparse.ArgumentParser(
    description="Данный скрипт поможет залить файл подкаста, сгенерировать обложку, срендерить и залить видео на ютуб и приготовить текст поста на сайт"
)

parser.add_argument(
    "-i",
    "--img",
    dest="img",
    action="store",
    default=None,
    help="Файл с изображением подкаста",
)
parser.add_argument(
    "-m",
    "--mp3",
    dest="mp3",
    action="store",
    help="Файл с mp3 подкаста",
)
parser.add_argument(
    "-t",
    "--title",
    dest="title",
    action="store",
    required=True,
    help="Название подкаста",
)
parser.add_argument(
    "-d",
    "--description",
    dest="description_file",
    action="store",
    default="description.html",
    help="Файл с описанием подкаста. По умолчанию: description.html",
)

parser.add_argument(
    "--announce",
    dest="announce",
    action="store",
    help="Указать, если нужно опубликовать анонс. Необходимо указать дату подкаста в формате 20210718T140000",
)

if __name__ == "__main__":
    args = parser.parse_args()

    print(f"Изображение подкаста: {args.img}")
    print(f"Файл подкаста: {args.mp3}")
    print(f"Название: {args.title}")
    print(f"Файл с описанием: {args.description_file}")
    print("=" * screen_width)

    main()

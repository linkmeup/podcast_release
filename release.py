#!/usr/bin/env python3
from html.parser import HTMLParser
import os
import shutil
import argparse
import decouple
import logging

import logger
from gen_cover import gen_cover, prepare_rss_cover, prepare_vk_cover
from yt import upload_video, update_playlist
from render_video import render_video
from fs import copy_file

screen_width, _ = shutil.get_terminal_size()
screen_width -= 1

FS = 'fs.linkmeup.ru'
FS_PATH = decouple.config('FS_PATH')

PODTRAC_BASE = 'https://dts.podtrac.com/redirect.mp3'

FEEDS  = {
    "LTE": "lte",
    "telecom": "telecom",
    "sysadmins": "sysadmin",
    "По'уехавшие": "pouekhavshie",
    "Шоты": "shorts",
    "IRL": "irl",
    "Поjncieлки": "ccielki",
    "Поrhcaлки": "ccielki",
    "Поallелки": "ccielki",
    "Поccieлки": "ccielki",
    "По'училки": "ccielki",
    "linkmeup": "other",
}


class HTMLFilter(HTMLParser):
    text = ''
    def handle_data(self, data):
        self.text += data


class Podcast():
    def __init__(self, title, description, mp3, img=None):
        self.title = title
        self.description = description
        self.feed = self.get_feed()
        
        self.filename_pattern = mp3.split('/')[-1].split('.')[0]
        self.mp3 = mp3

        self.mp3_filename = f'{self.filename_pattern}.mp3'

        if img:
            self.img = img
        else:
            self.img = f'img/defaults/{podcast.feed}_img.png'
        
        if not os.path.exists(self.img):
            raise ValueError(f'Файл {self.img} не существует')

        img_extension = img.split('.')[-1]
        self.img_filename = f'{self.filename_pattern}.{img_extension}'

    def get_feed(self) -> str:
        first_word = self.title.split()[0]
        return FEEDS[first_word] if FEEDS[first_word] else 'other'

    def create_covers(self):
        self.cover = gen_cover(self)
        self.cover_filename = self.cover.split('/')[-1]

        self.rss_cover = prepare_rss_cover(self)
        self.rss_cover_filename = self.rss_cover.split('/')[-1]

        self.vk_cover = prepare_vk_cover(self)
        self.vk_cover_filename = self.vk_cover.split('/')[-1]


    def mp3_upload(self):
        os.chmod(self.mp3, 0o644)
        file_path = f'podcasts/{self.feed}/{self.mp3_filename}'
        full_path = f'{FS_PATH}/{file_path}'
        copy_file(self.mp3, full_path)
        self.podtrac_url = f'{PODTRAC_BASE}/{FS}/{file_path}'

    def img_upload(self):
        os.chmod(self.img, 0o644)
        file_path = f'images/{self.img_filename}'
        full_path = f'{FS_PATH}/{file_path}'
        copy_file(self.img, full_path)
        self.img_url = f'https://{FS}/{file_path}'

    def cover_upload(self):
        os.chmod(self.cover, 0o644)
        file_path = f'images/{self.cover_filename}'
        full_path = f'{FS_PATH}/{file_path}'
        copy_file(self.cover, full_path)
        self.cover_url = f'https://{FS}/{file_path}'

    def rss_cover_upload(self):
        os.chmod(self.rss_cover, 0o644)
        file_path = f'images/{self.rss_cover_filename}'
        full_path = f'{FS_PATH}/{file_path}'
        copy_file(self.rss_cover, full_path)
        self.rss_cover_url = f'https://{FS}/{file_path}'

    def render(self):
        self.mp4 = render_video(self)

    def yt_upload(self):
        self.yt_id = upload_video(self)
        update_playlist(self)
        self.yt_url = f'https://www.youtube.com/watch?v={self.yt_id}'

    @property
    def nice_view(self) -> str:

        output = '=' * screen_width
        output += format_output(' title', self.title)
        output += format_output('feed', self.feed)
        output += format_output('mp3', self.mp3)
        output += format_output('mp3_file', self.mp3_filename)

        if hasattr(self, 'img'):
            output += format_output('img', self.img)
            output += format_output('img_file', self.img_filename)

        if hasattr(self, 'img_url'):
            output += format_output('img url', self.img_url)

        if hasattr(self, 'cover'):
            output += format_output('cover', self.cover)
            output += format_output('cover_filename', self.cover_filename)

        if hasattr(self, 'cover_url'):
            output += format_output('cover url', self.cover_url)

        if hasattr(self, 'rss_cover'):
            output += format_output('rss_cover', self.rss_cover)
            output += format_output('rss_cover_filename', self.rss_cover_filename)

        if hasattr(self, 'rss_cover_url'):
            output += format_output('rss_cover url', self.rss_cover_url)

        if hasattr(self, 'vk_cover'):
            output += format_output('vk_cover', self.vk_cover)
            output += format_output('vk_cover_filename', self.vk_cover_filename)


        if hasattr(self, 'podtrac_url'):
            output += format_output('podcast url', self.podtrac_url)

        if hasattr(self, 'mp4'):
            output += format_output('mp4', self.mp4)

        if hasattr(self, 'yt_id'):
            output += format_output('youtube id', self.yt_id)
            output += format_output('youtube url', self.yt_url)

        output += format_output('description', self.description)
        # output += format_output("youtube body", self.yt_body)

        output += '=' * screen_width

        return output

    @property
    def site_view(self) -> str:

        output = '=' * screen_width
        output += '\n'
        output += 'title\n' + self.title
        output += '\n'
        output += '-' * screen_width
        output += '\n'

        if hasattr(self, 'podtrac_url'):
            output += 'podcast url\n' + self.podtrac_url
            output += '\n'
            output += '-' * screen_width
            output += '\n'

        if not hasattr(self, 'yt_url'):
            self.yt_url = ''

        output += 'description\n'
        output += '-----------\n' + self.site_body
        output += '=' * screen_width

        return output

    @property
    def yt_body(self) -> str:

        f = HTMLFilter()
        f.feed(self.description)
        
        return f.text + '''


        ------------------------------------------------------------
        Канал в телеграме: https://t.me/linkmeup_podcast​
        Подкаст доступен в iTunes, Google Подкастах, Яндекс Музыке, Castbox
        Сообщество в вк: https://vk.com/linkmeup​
        Группа в фб: https://www.facebook.com/linkmeup.sdsm​
        Группа в linkedin: https://www.linkedin.com/groups/5076111​
        Пообщаться в общих чатах в тг:
        - https://t.me/linkmeup_chat
        - https://t.me/linkmeup_sysadm_chat​

        Поддержите проект:
        https://www.patreon.com/linkmeup
        ------------------------------------------------------------
    '''

    @property
    def site_body(self) -> str:

        return self.description + f'''

<video>{self.yt_url}</video>

<audio controls>
  <source src="{self.podtrac_url}" type="audio/mp3">
</audio>

<blockquote>
Канал в телеграме: <a href="https://t.me/linkmeup_podcast">t.me/linkmeup_podcast</a>
Канал на youtube: <a href="https://youtube.com/c/linkmeup-podcast">youtube.com/c/linkmeup-podcast</a>
Подкаст доступен в <a href="https://itunes.apple.com/ru/podcast/linkmeup.-pervyj-podkast-dla/id1065445951?mt=2">iTunes</a>, <a href="https://podcasts.google.com/feed/aHR0cHM6Ly9saW5rbWV1cC5ydS9yc3MvcG9kY2FzdHM">Google Подкастах</a>, <a href="https://music.yandex.ru/album/7060168">Яндекс Музыке</a>, <a href="https://castbox.fm/channel/linkmeup.-Подкаст-про-IT-и-про-людей-id1173801?country=ru">Castbox</a>
Сообщество в вк: <a href="https://vk.com/linkmeup">vk.com/linkmeup</a>
Группа в фб: <a href="https://www.facebook.com/linkmeup.sdsm/">www.facebook.com/linkmeup.sdsm</a>
Группа в linkedin: <a href="https://www.linkedin.com/groups/5076111​">https://www.linkedin.com/groups/5076111​</a>

Скачать все выпуски подкаста вы можете с <a href="https://yadi.sk/d/exFFAsItbePoV">яндекс-диска</a>.
Добавить <a href="https://linkmeup.ru/rss/podcasts">RSS</a> в подкаст-плеер.

Пообщаться в общем чате в тг: https://t.me/linkmeup_chat 

Поддержите проект:
<a href="https://www.patreon.com/linkmeup?ty=h" target="_blank"><img src="https://fs.linkmeup.ru/images/patreon.jpg" align="center" title="Поддержать нас на Patreon" width="300"></a>
</blockquote>
'''


def format_output(text: str, value: str) -> str:
    return f'{text + ":": <20}{value}\n'


def main():

    # Initialize logger
    logger.init_logging(0)
    log = logging.getLogger(__name__)

    with open(args.description_file, 'r') as f:
        description = f.read()

    podcast = Podcast(args.title, description, args.mp3, args.img)

    # Generate podcast cover
    log.delimiter('=' * screen_width)
    log.topic('Рисуем обложки')
    podcast.create_covers()
    log.info('  Готово.')

    # Upload files to file-hosting
    log.delimiter('-' * screen_width)
    log.topic('Загружаем mp3 на fs')
    podcast.mp3_upload()
    log.info('\n  Готово.')

    log.delimiter('-' * screen_width)
    log.topic('Загружаем изображение выпуска на fs')
    podcast.img_upload()
    log.info('\n  Готово.')

    log.delimiter('-' * screen_width)
    log.topic('Загружаем обложку выпуска на fs')
    podcast.cover_upload()
    log.info('\n  Готово.')

    log.delimiter('-' * screen_width)
    log.topic('Загружаем обложку выпуска для RSS на fs')
    podcast.rss_cover_upload()
    log.info('\n  Готово.')

    # Render video by ffmpeg
    log.delimiter('-' * screen_width)
    log.topic('Рендерим видео')
    podcast.render()
    log.info('  Готово.')

    # Upload video to youtube in private mode, add to playlist
    log.delimiter('-' * screen_width)
    log.topic('Загружаем видео на Youtube')
    podcast.yt_upload()
    log.info('  Готово.')

    log.info(podcast.nice_view)
    # print(podcast.site_view)

    # TBD. Create post on site

parser = argparse.ArgumentParser(
    description='Данный скрипт поможет залить файл подкаста, сгенерировать обложку, срендерить и залить видео на ютуб и приготовить текст поста на сайт'
)

parser.add_argument(
    '-i', '--img',
    dest='img',
    action='store',
    default=None,
    help='Файл с изображением подкаста',
)
parser.add_argument(
    '-m', '--mp3',
    dest='mp3',
    action='store',
    required=True,
    help='Файл с mp3 подкаста',
)
parser.add_argument(
    '-t','--title',
    dest='title',
    action='store',
    required=True,
    help='Название подкаста',
)
parser.add_argument(
    '-d', '--description',
    dest='description_file',
    action='store',
    default='description.html',
    # required=True,
    help='Файл с описанием подкаста. По умолчанию: description.html',
)

if __name__ == '__main__':
    args = parser.parse_args()
    main()

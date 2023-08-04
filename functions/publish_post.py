import http.client
import json
from datetime import datetime

from constants import (
    ICS_DIR,
    EVENT_TEMPLATE_FILE,
    PODCAST_CATEGORIES,
    SITE_SECRET,
)
from functions.s3 import copy_file


def make_event(podcast):
    with open(EVENT_TEMPLATE_FILE) as f:
        event_template = f.read()

    start_time = podcast.date
    date, time = start_time.split("T")
    time = int(time) + 20000

    end_time = f"{date}T{time}"
    event = event_template.format(start_time, end_time, podcast.title)

    # ics = f"{ICS_DIR}/{podcast.feed}.ics"
    # with open(ics, "w") as f:
    #     f.write(event)

    # file_path = f"calendar/{podcast.feed}.ics"
    # # full_path = f"file_path}"
    # # print(ics, file_path, full_path)

    # # copy_file(ics, full_path)
    # copy_file(ics, file_path)


def publish_post(podcast, announce=False):
    conn = http.client.HTTPSConnection("linkmeup.ru")
    headers = {
        "Authorization": f"Basic {SITE_SECRET}",
        "Content-Type": "application/json",
    }

    if announce:
        payload, url = prepare_announce(podcast)
    else:
        payload, url = prepare_podcast(podcast)

    conn.request("POST", url, payload, headers)
    res = conn.getresponse()
    data = res.read()
    try:
        result = json.loads(data.decode("utf-8"))["permalink_template"].replace(
            "\\", ""
        )
    except Exception as e:
        result = str(e)
    return result


def prepare_podcast(podcast):
    payload = json.dumps(
        {
            "title": podcast.title,
            "excerpt": podcast.excerpt,
            "content": podcast.site_body.replace("\n", "<p></p>"),
            "status": "draft",
            "podcast-category": [PODCAST_CATEGORIES[podcast.feed]],
            "podcast_image_url": podcast.img_url,
            "podcast_audio_url": podcast.podtrac_url,
        }
    )
    url = "/wp-json/wp/v2/podcasts/"
    return payload, url


def prepare_announce(podcast):
    make_event(podcast)
    # date = datetime.strptime(podcast.date, "%Y%m%dT%H%M%S").strftime("%Y.%m.%d %H:%M")
    date = datetime.strptime(podcast.date, "%d%m%YT%H%M%S").strftime("%d.%m.%Y %H:%M")
    post_body = (
        f"<img src='{podcast.cover_url}'>\n"
        + podcast.description
        + f"""\n
<b>Когда:</b> {date}. <a href="https://s3.linkmeup.ru/linkmeup/calendar/{podcast.feed}.ics">Событие в календаре</a>\n
"""
    )
    if "анонс" not in podcast.title.lower():
        podcast.title = f"Анонс {podcast.title}"
    payload = json.dumps(
        {
            "title": podcast.title,
            "excerpt": podcast.excerpt,
            "content": post_body.replace("\n", "<p></p>"),
            "status": "draft",
            "article-category": [13],
            "article_image_url": podcast.img_url,
            "event_date": date,
        }
    )
    url = "/wp-json/wp/v2/blog/"
    return payload, url

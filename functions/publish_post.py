import http.client
import json
from datetime import datetime

from constants import PODCAST_CATEGORIES, SITE_SECRET


def make_event(podcast):
    # TBD Make google cal event
    return


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
    date = datetime.strptime(podcast.date, "%d%m%YT%H%M%S").strftime("%d.%m.%Y %H:%M")
    post_body = (
        f"<img src='{podcast.cover_url}'>\n"
        + podcast.description
        + f"""\n
<b>Когда:</b> {date}. <a href="https://calendar.google.com/calendar/u/0?cid=ZmZkYjFjNzUyNzllZGQzYmFiZjhlODAwNjU3Y2Q0MDM5NDFmOTUxZmQzMzc5NDhhNjZjNmUwMjUwNjdhNDZmMkBncm91cC5jYWxlbmRhci5nb29nbGUuY29t">Ссылка на гугл-календарь</a>.
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

import http.client
import json

import decouple

SECRET = decouple.config("SITE_SECRET")

PODCAST_CATEGORIES = {
    "IRL": 9,
    "lte": 6,
    "sysadmins": 4,
    "telecom": 3,
    "по'ехавшие": 5,
    "поccieлки": 8,
    "шоты": 7,
}


def publish_post(podcast):
    conn = http.client.HTTPSConnection("linkmeup.ru")
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

    headers = {"Authorization": f"Basic {SECRET}", "Content-Type": "application/json"}
    conn.request("POST", "/wp-json/wp/v2/podcasts/", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))["permalink_template"].replace("\\", "")

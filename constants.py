import decouple

SITE_SECRET = decouple.config("SITE_SECRET")

PODTRAC_BASE = "https://dts.podtrac.com/redirect.mp3"
S3_ENDPOINT = "https://s3.linkmeup.ru"
S3_BUCKET = "linkmeup"
S3_SECRET = decouple.config('AWS_SECRET')

ICS_DIR = "ics"
EVENT_TEMPLATE_FILE = f"{ICS_DIR}/event_template.ics"

FEEDS = {
    "LTE": "lte",
    "telecom": "telecom",
    "sysadmins": "sysadmins",
    "По'уехавшие": "pouekhavshie",
    "pouekhavshie": "pouekhavshie",
    "Шоты": "shorts",
    "IRL": "irl",
    "Поjncieлки": "ccielki",
    "Поrhcaлки": "ccielki",
    "Поallелки": "ccielki",
    "Поccieлки": "ccielki",
    "По'училки": "ccielki",
    "linkmeup": "other",
}

PODCAST_CATEGORIES = {
    "irl": 9,
    "lte": 6,
    "sysadmins": 4,
    "telecom": 3,
    "по'уехавшие": 5,
    "pouekhavshie": 5,
    "поccieлки": 8,
    "шоты": 7,
    "shorts": 7,
    "other": 7,
}

FONT = "fonts/Lato-Bold.ttf"

YT_CATEGORY_ID = 28
YT_TAGS = ["linkmeup", "networking", "technology", "podcast", "подкасты"]
YT_CLIENT_SECRETS = "client_secrets.json"
YT_OAUTH_PATH = "oauth.json"

UPLOAD_BODY_TEMPLATE = {
    "snippet": {
        "categoryId": 28,
        "title": "",
        "description": "",
        "tags": ["linkmeup", "networking", "technology", "podcast", "подкасты"],
    },
    "status": {"privacyStatus": "private", "selfDeclaredadeForKids": False},
}

PLAYLIST_BODY_TEMPLATE = {
    "snippet": {
        "playlistId": "",
        "position": 0,
        "resourceId": {"kind": "youtube#video", "videoId": ""},
    }
}

PLAYLIS_IDS = {
    "telecom": "PLHN9m7XN8U8HPjkJ-0PpZ493xNvQoFyFc",
    "sysadmins": "PLHN9m7XN8U8HM90YNcLRc8-_MBI4lCsSO",
    "lte": "PLHN9m7XN8U8HUvXi0bB6lGTJ5K8yOPR6q",
    "poccielki": "PLHN9m7XN8U8H22Xpmd-sMjTiS0woNLKaA",
    "emigration": "PLHN9m7XN8U8EqpFFiQoFJ9NVJvi2VU7Hj",
    "irl": "PLHN9m7XN8U8EKXAoSlpbgmdjbOYd78BM0",
    "shorts": "PLHN9m7XN8U8EfgSMi9Es6TuLCLJgjL9g5",
    "other": "PLHN9m7XN8U8G2bDGE66-JVsV3fezZnZtC",
}

import decouple

FS = "fs.linkmeup.ru"
FS_PATH = decouple.config("FS_PATH")

PODTRAC_BASE = "https://dts.podtrac.com/redirect.mp3"

FEEDS = {
    "LTE": "lte",
    "telecom": "telecom",
    "sysadmins": "sysadmins",
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

PODCAST_CATEGORIES = {
    "IRL": 9,
    "lte": 6,
    "sysadmins": 4,
    "telecom": 3,
    "по'ехавшие": 5,
    "поccieлки": 8,
    "шоты": 7,
}

FONT = "Lato-Bold.ttf"

CLIENT_SECRETS_FILE = "client_secrets.json"

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

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

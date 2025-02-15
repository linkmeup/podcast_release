import decouple

SITE_SECRET = decouple.config("SITE_SECRET")

S3_ENDPOINT = "https://s3.linkmeup.ru"
S3_BUCKET = "linkmeup"
S3_SECRET = decouple.config("AWS_SECRET")

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
    "До": "donasdoshlo",
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
    "donasdoshlo": 188,
}

FONT = "fonts/Lato-Bold.ttf"
FONT_DOSHLO_1 = "fonts/11662.ttf"
FONT_DOSHLO_2 = "fonts/11664.ttf"

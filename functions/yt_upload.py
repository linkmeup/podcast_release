import copy
import os

from youtube_upload.client import YoutubeUploader

from constants import (
    PLAYLIS_IDS,
    PLAYLIST_BODY_TEMPLATE,
    YT_CATEGORY_ID,
    YT_CLIENT_SECRETS,
    YT_OAUTH_PATH,
    YT_TAGS,
)

uploader = YoutubeUploader(secrets_file_path=YT_CLIENT_SECRETS)

uploader.authenticate(oauth_path=YT_OAUTH_PATH)


def upload_video(podcast) -> str:

    if not os.path.exists(podcast.mp4):
        raise ValueError(f"Файл {podcast.mp4} не существует.")

    options = {
        "title": podcast.title,
        "description": podcast.yt_body,
        "categoryId": YT_CATEGORY_ID,
        "tags": YT_TAGS,
        "privacyStatus": "private",  # Video privacy. Can either be "public", "private", or "unlisted"
        "kids": False,  # Specifies if the Video if for kids or not. Defaults to False.
    }

    upload_reponse = uploader.upload(podcast.mp4, options)

    return upload_reponse[0]["id"]


def update_playlist(podcast):

    if podcast.feed in PLAYLIS_IDS:
        playlist_id = PLAYLIS_IDS[podcast.feed]
    else:
        playlist_id = PLAYLIS_IDS["other"]

    playlist_body = copy.deepcopy(PLAYLIST_BODY_TEMPLATE)
    playlist_body["snippet"]["playlistId"] = playlist_id
    playlist_body["snippet"]["resourceId"]["videoId"] = podcast.yt_id

    uploader.add_to_playlist(playlist_body)

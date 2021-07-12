import copy
import os

import google_auth_oauthlib.flow
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from constants import (API_SERVICE_NAME, API_VERSION, CLIENT_SECRETS_FILE,
                       PLAYLIS_IDS, PLAYLIST_BODY_TEMPLATE, SCOPES,
                       UPLOAD_BODY_TEMPLATE)


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


service = get_authenticated_service()


def upload_video(podcast) -> str:

    if not os.path.exists(podcast.mp4):
        raise ValueError(f"Файл {podcast.mp4} не существует.")

    media_file = MediaFileUpload(podcast.mp4)

    upload_body = copy.deepcopy(UPLOAD_BODY_TEMPLATE)
    upload_body["snippet"]["title"] = podcast.title
    upload_body["snippet"]["description"] = podcast.yt_body
    upload_body["snippet"]["tags"].append(podcast.feed)

    while True:
        try:
            upload_request = (
                service.videos()
                .insert(part="snippet,status", body=upload_body, media_body=media_file)
                .execute()
            )
            return upload_request["id"]

        except Exception as e:
            print(e)


def update_playlist(podcast):

    if podcast.feed in PLAYLIS_IDS:
        playlist_id = PLAYLIS_IDS[podcast.feed]
    else:
        playlist_id = PLAYLIS_IDS["other"]

    playlist_body = copy.deepcopy(PLAYLIST_BODY_TEMPLATE)
    playlist_body["snippet"]["playlistId"] = playlist_id
    playlist_body["snippet"]["resourceId"]["videoId"] = podcast.yt_id

    playlist_request = (
        service.playlistItems().insert(part="snippet", body=playlist_body).execute()
    )

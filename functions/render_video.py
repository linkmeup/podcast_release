import os
import subprocess

import psutil


def render_video(podcast, need_render) -> str:

    if not os.path.exists(podcast.mp3):
        raise ValueError(f"Файл {podcast.mp3} не существует.")

    if not os.path.exists(podcast.cover):
        raise ValueError(f"Файл {podcast.cover} не существует.")

    video_file_name = f"mp4/{podcast.filename}.mp4"

    if need_render:
        cmd = f'ffmpeg -loop 1 -i "{podcast.cover}" -i "{podcast.mp3}" -c:a copy -c:v libx264 -shortest "{video_file_name}"'
        push = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

        while True:
            if psutil.Process(push.pid).status() == "zombie":
                break

    return video_file_name

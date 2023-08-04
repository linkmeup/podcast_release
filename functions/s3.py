import os
import sys
import threading

import boto3
from boto3.s3.transfer import TransferConfig
from botocore.client import Config

from constants import S3_BUCKET, S3_ENDPOINT, S3_SECRET


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify, assume this is hooked up to a single filename
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)"
                % (self._filename, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()


def copy_file(local_file, remote_file, content_type):
    s3 = boto3.resource(
        "s3",
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=S3_BUCKET,
        aws_secret_access_key=S3_SECRET,
        config=Config(signature_version="s3v4"),
    )

    GB = 1024**3
    config = TransferConfig(multipart_threshold=5 * GB)

    print(remote_file)

    s3.Bucket(S3_BUCKET).upload_file(
        local_file, remote_file, Config=config, Callback=ProgressPercentage(local_file), ExtraArgs={'ContentType': content_type}
    )

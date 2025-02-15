#!/usr/bin/env python3
import sys
from os import listdir
from os.path import isfile, join

from constants import S3_BUCKET, S3_ENDPOINT
from functions.s3 import copy_file

mypath = "upload_files"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
print(onlyfiles)

file_path = f"images/{sys.argv[1]}"
for file in onlyfiles:
    if file in ["upload_files.py", ".DS_Store"]:
        continue
    copy_file(f"{mypath}/{file}", f"{file_path}/{file}", "image/png")
    print()
    print(f"{S3_ENDPOINT}/{S3_BUCKET}/{file_path}/{file}")

# audio/mpeg

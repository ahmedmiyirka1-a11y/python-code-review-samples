"""
Utility script to read, back up, and delete uploaded files.
"""

import os
import shutil


UPLOAD_DIR = "uploads"
BACKUP_DIR = "backups"


def read_file(filename):
    path = UPLOAD_DIR + "/" + filename
    f = open(path, "r")
    content = f.read()
    return content


def backup_file(filename):
    src = UPLOAD_DIR + "/" + filename
    dst = BACKUP_DIR + "/" + filename
    shutil.copy(src, dst)
    print("Backed up " + filename)


def delete_file(filename):
    path = UPLOAD_DIR + "/" + filename
    os.remove(path)
    print("Deleted " + filename)


def write_log(message):
    f = open("activity.log", "a")
    f.write(message + "\n")


def process_upload(filename):
    content = read_file(filename)
    word_count = len(content.split(" "))

    backup_file(filename)
    write_log(f"Processed {filename}, {word_count} words")

    if word_count == 0:
        delete_file(filename)

    return word_count


def process_all_uploads():
    files = os.listdir(UPLOAD_DIR)
    total_words = 0

    for filename in files:
        total_words += process_upload(filename)

    print("Total words processed: " + str(total_words))


if __name__ == "__main__":
    process_all_uploads()

"""
Utility script to read, back up, and delete uploaded files
(fixed / production-ready version).
"""

import logging
import os
import shutil

UPLOAD_DIR = "uploads"
BACKUP_DIR = "backups"
LOG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "activity.log")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def safe_path(base_dir: str, filename: str) -> str:
    """Resolve filename inside base_dir, rejecting path traversal."""
    base_dir_abs = os.path.abspath(base_dir)
    full_path = os.path.abspath(os.path.join(base_dir_abs, filename))
    if not full_path.startswith(base_dir_abs + os.sep):
        raise ValueError(f"Invalid filename: {filename}")
    return full_path


def read_file(filename: str) -> str:
    """Read and return the contents of a file inside UPLOAD_DIR."""
    path = safe_path(UPLOAD_DIR, filename)
    with open(path, "r") as f:
        return f.read()


def backup_file(filename: str) -> None:
    """Copy a file from UPLOAD_DIR to BACKUP_DIR, creating it if needed."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    src = safe_path(UPLOAD_DIR, filename)
    dst = safe_path(BACKUP_DIR, filename)
    shutil.copy(src, dst)
    logger.info("Backed up %s", filename)


def delete_file(filename: str) -> None:
    """Delete a file from UPLOAD_DIR."""
    path = safe_path(UPLOAD_DIR, filename)
    os.remove(path)
    logger.info("Deleted %s", filename)


def write_log(message: str) -> None:
    """Append a message to the activity log."""
    with open(LOG_PATH, "a") as f:
        f.write(message + "\n")


def process_upload(filename: str, delete_if_empty: bool = False) -> int:
    """
    Read an uploaded file, back it up, log the activity, and return its
    word count. Deletion of empty files is opt-in via delete_if_empty.
    """
    try:
        content = read_file(filename)
    except (FileNotFoundError, PermissionError, ValueError) as e:
        logger.warning("Could not read %s: %s", filename, e)
        return 0

    word_count = len(content.split())

    try:
        backup_file(filename)
    except OSError as e:
        logger.warning("Could not back up %s: %s", filename, e)

    write_log(f"Processed {filename}, {word_count} words")

    if word_count == 0 and delete_if_empty:
        try:
            delete_file(filename)
        except OSError as e:
            logger.warning("Could not delete %s: %s", filename, e)

    return word_count


def process_all_uploads(delete_empty_files: bool = False) -> int:
    """Process every file in UPLOAD_DIR and return the total word count."""
    if not os.path.isdir(UPLOAD_DIR):
        logger.error("Upload directory not found: %s", UPLOAD_DIR)
        return 0

    total_words = 0
    for filename in os.listdir(UPLOAD_DIR):
        total_words += process_upload(filename, delete_if_empty=delete_empty_files)

    print(f"Total words processed: {total_words}")
    return total_words


if __name__ == "__main__":
    process_all_uploads()

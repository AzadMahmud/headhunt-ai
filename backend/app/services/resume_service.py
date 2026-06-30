from pathlib import Path
from fastapi import UploadFile


UPLOAD_DIR = Path("uploads")


def save_resume(file: UploadFile) -> Path:
    """
    Save uploaded resume to disk.
    """

    UPLOAD_DIR.mkdir(exist_ok=True)

    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        buffer.write(file.file.read())

    return destination
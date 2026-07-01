from pathlib import Path
import uuid
from fastapi import UploadFile


UPLOAD_DIR = Path("uploads")


def save_resume(file: UploadFile) -> Path:
    """
    Save uploaded resume to disk.
    """

    UPLOAD_DIR.mkdir(exist_ok=True)

    suffix = Path(file.filename).suffix

    unique_filename = f"{uuid.uuid4()}{suffix}"

    destination = UPLOAD_DIR / unique_filename

    with destination.open("wb") as buffer:
        buffer.write(file.file.read())

    return destination
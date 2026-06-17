from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".csv", ".json"}

def validate_file_extension(filename: str) -> None:
    extention = Path(filename).suffix.lower()

    if extention not in ALLOWED_EXTENSIONS:
        raise ValueError("Only CSV and JSON files are allowed.")

def save_uploaded_file(file: UploadFile) -> str:
    validate_file_extension(file.filename)

    extension = Path(file.filename).suffix.lower()
    unique_filename = f"{uuid4()}{extension}"
    file_path = UPLOAD_DIR / unique_filename

    UPLOAD_DIR.mkdir(exist_ok=True)

    with file_path.open("wb") as buffer:
        buffer.write(file.file.read())

    return str(file_path)

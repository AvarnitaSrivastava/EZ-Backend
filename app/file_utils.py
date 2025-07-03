import os
from fastapi import UploadFile
from uuid import uuid4

FILES_DIR = "files"
os.makedirs(FILES_DIR, exist_ok=True)

def save_upload_file(upload_file: UploadFile) -> str:
    ext = upload_file.filename.rsplit(".", 1)[-1].lower()
    unique_name = f"{uuid4().hex}.{ext}"
    file_path = os.path.join(FILES_DIR, unique_name)
    with open(file_path, "wb") as buffer:
        buffer.write(upload_file.file.read())
    return unique_name

def get_file_path(filename: str) -> str:
    file_path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {filename} not found.")
    return file_path 
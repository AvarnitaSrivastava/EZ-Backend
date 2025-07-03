import secrets
import string
from fastapi import HTTPException, status, UploadFile

ALLOWED_EXTENSIONS = {"pptx", "docx", "xlsx"}

def validate_file_extension(file: UploadFile):
    filename = file.filename
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return ext

def generate_secure_token(length=32):
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length)) 
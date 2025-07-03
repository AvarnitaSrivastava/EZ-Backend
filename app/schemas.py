from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    role: str
    is_verified: bool
    created_at: datetime
    class Config:
        from_attributes: True

class FileOut(BaseModel):
    id: int
    filename: str
    uploader_id: int
    upload_time: datetime
    class Config:
        from_attributes: True

class DownloadTokenOut(BaseModel):
    download_link: str
    message: str = "success"

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None 
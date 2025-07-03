from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app import models, schemas, auth, utils, file_utils, email_utils
from datetime import datetime, timedelta
from fastapi.responses import FileResponse

router = APIRouter(prefix="/client", tags=["Client"])

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(auth.get_db), request: Request = None):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, password_hash=hashed, role="client", is_verified=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    token = auth.create_access_token({"sub": db_user.email, "role": db_user.role}, expires_delta=timedelta(hours=1))
    verify_url = f"{request.base_url}client/verify-email?token={token}"
    email_utils.send_verification_email(db_user.email, verify_url)
    return {"verification_url": verify_url}

@router.get("/verify-email")
def verify_email(token: str, db: Session = Depends(auth.get_db)):
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_verified = True
    db.commit()
    return {"message": "Email verified successfully"}

@router.post("/login", response_model=schemas.Token)
def client_login(form_data: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if user.role != "client":
        raise HTTPException(status_code=403, detail="Not a client user")
    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Email not verified")
    access_token = auth.create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/files", response_model=list[schemas.FileOut])
def list_files(db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.require_role("client"))):
    files = db.query(models.File).all()
    return files

@router.post("/download-file/{file_id}", response_model=schemas.DownloadTokenOut)
def get_download_link(file_id: int, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.require_role("client"))):
    file = db.query(models.File).filter(models.File.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    token = utils.generate_secure_token()
    expires_at = datetime.utcnow() + timedelta(minutes=15)
    db_token = models.DownloadToken(file_id=file.id, client_id=current_user.id, token=token, expires_at=expires_at, used=False)
    db.add(db_token)
    db.commit()
    download_link = f"/client/download/{token}"
    return {"download_link": download_link, "message": "success"}

@router.get("/download/{token}")
def download_file(token: str, db: Session = Depends(auth.get_db), current_user: models.User = Depends(auth.require_role("client"))):
    db_token = db.query(models.DownloadToken).filter(models.DownloadToken.token == token).first()
    if not db_token or db_token.used:
        raise HTTPException(status_code=404, detail="Invalid or expired download link")
    if db_token.client_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized for this download link")
    if db_token.expires_at < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Download link expired")
    db_token.used = True
    db.commit()
    file = db.query(models.File).filter(models.File.id == db_token.file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    file_path = file_utils.get_file_path(file.filename)
    return FileResponse(file_path, filename=file.filename) 
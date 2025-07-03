from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, auth, utils, file_utils

router = APIRouter(prefix="/ops", tags=["Ops"])

@router.post("/login", response_model=schemas.Token)
def ops_login(form_data: schemas.UserLogin, db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.email).first()
    if not user or not auth.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if user.role != "ops":
        raise HTTPException(status_code=403, detail="Not an Ops user")
    access_token = auth.create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/upload-file", status_code=201)
def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(auth.get_db),
    current_user: models.User = Depends(auth.require_role("ops"))
):
    utils.validate_file_extension(file)
    filename = file_utils.save_upload_file(file)
    db_file = models.File(filename=filename, uploader_id=current_user.id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return {"file_id": db_file.id, "filename": db_file.filename} 
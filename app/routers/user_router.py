import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.database import SessionLocal, engine
from app.database import crud, models, schemas
from app.utils.auth import authenticate_user, get_current_user

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

UPLOAD_DIR = "/media/avatars"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user


@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/users/me", response_model=schemas.User)
def update_user(
        user_update: schemas.UserUpdate,
        db: Session = Depends(get_db),
        current_user: schemas.User = Depends(get_current_user),
):
    db_user = crud.get_user(db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = crud.update_user(db=db, db_user=db_user, user_update=user_update)
    return updated_user


@router.post("/upload-avatar/")
async def upload_avatar(user_id: str, file: UploadFile = File(...)):
    file_location = f"{UPLOAD_DIR}/{user_id}.png"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    return {"info": "Avatar uploaded successfully"}


@router.get("/avatars/{user_id}")
async def get_avatar(user_id: str):
    file_location = f"{UPLOAD_DIR}/{user_id}.png"
    if Path(file_location).exists():
        return FileResponse(file_location)
    raise HTTPException(status_code=404, detail="Avatar not found")

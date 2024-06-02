from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        avatar_url=user.avatar_url,  # Add this line
        name=user.name,
        persona=user.persona or {}  # Handle persona being None
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: models.User, user_update: schemas.UserUpdate):
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "persona":
            db_user.persona.update(value)
        else:
            setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


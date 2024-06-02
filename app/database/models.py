from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from . import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    avatar_url = Column(String, nullable=True)
    persona = Column(JSONB, nullable=True, default={
        'age': '25',
        'occupation': 'Software Developer',
        'tech_level': 'Advanced',
        'main_goals': 'Improve coding skills, learn new technologies',
        'interests': 'AI, Machine Learning, Open Source Projects',
        'usage_pattern': 'Frequent, mostly evenings and weekends',
        'position': 'Member',
        'role': 'user'
    })  # 사용자의 페르소나

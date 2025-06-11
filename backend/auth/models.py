from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    subscription = Column(String, default="free")
    usage = Column(Integer, default=0)
    quota_reset = Column(DateTime, default=datetime.utcnow)
    spotify_token = Column(String, nullable=True)
    youtube_token = Column(String, nullable=True)
    soundcloud_token = Column(String, nullable=True)

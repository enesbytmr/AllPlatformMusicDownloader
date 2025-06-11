from sqlalchemy import Column, Integer, String

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    subscription = Column(String, default="free")
    spotify_token = Column(String, nullable=True)
    youtube_token = Column(String, nullable=True)
    soundcloud_token = Column(String, nullable=True)

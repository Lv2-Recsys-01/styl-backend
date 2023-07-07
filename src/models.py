from passlib.context import CryptContext
from sqlalchemy import (ARRAY, Column, DateTime, ForeignKey, Integer,
                        String, CHAR, Boolean)
from sqlalchemy.orm import relationship

from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    user_pwd = Column(String)

    likes = relationship("Like", back_populates="user")
    clicks = relationship("Click", back_populates="user")
    session = relationship("Session", back_populates="user")

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.login_pwd)

    def hash_password(self, plain_password):
        self.login_pwd = pwd_context.hash(plain_password)


class Outfit(Base):
    __tablename__ = "outfit"

    outfit_id = Column(Integer, primary_key=True, index=True)
    gender = Column(CHAR(2))
    age = Column(Integer)
    img_url = Column(String)
    origin_url = Column(String)
    reporter = Column(String)
    tags = Column(ARRAY(String))
    brands = Column(ARRAY(String))
    region = Column(String)
    occupation = Column(String)
    style = Column(String)
    date = Column(DateTime, nullable=False)

    likes = relationship("Like", back_populates="outfit")
    clicks = relationship("Click", back_populates="outfit")
    similars = relationship("Similar", back_populates="outfit")


class Like(Base):
    __tablename__ = "like"

    like_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("session.session_id"))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"))
    timestamp = Column(DateTime, nullable=False)
    is_deleted = Column(Boolean)

    user = relationship("User", back_populates="likes")
    outfit = relationship("Outfit", back_populates="likes")
    session = relationship("Session", back_populates="likes")


class Click(Base):
    __tablename__ = "click"

    click_id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("session.session_id"))
    user_id = Column(Integer, ForeignKey("user.user_id"))
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"))
    timestamp = Column(DateTime, nullable=False)
    duration_secondes = Column(Integer)

    user = relationship("User", back_populates="clicks")
    outfit = relationship("Outfit", back_populates="clicks")
    session = relationship("Session", back_populates="clicks")


class Similar(Base):
    __tablename__ = "similar"

    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"), primary_key=True, index=True)
    similar_outfits = Column(ARRAY(Integer))

    outfit = relationship("Outfit", back_populates="similars")


class Session(Base):
    __tablename__ = "session"

    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    created_at = Column(DateTime)
    expired_at = Column(DateTime)

    user = relationship("User", back_populates="session")
    likes = relationship("Like", back_populates="user")
    clicks = relationship("Click", back_populates="user")

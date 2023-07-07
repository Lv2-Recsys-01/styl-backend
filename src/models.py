from passlib.context import CryptContext
from sqlalchemy import (ARRAY, Column, DateTime, Float, ForeignKey, Integer,
                        String, CHAR)
from sqlalchemy.orm import relationship

from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    login_id = Column(String, unique=True, index=True) # -> index 필요??
    login_pwd = Column(String)

    likes = relationship("Like", back_populates="user")
    clicks = relationship("Click", back_populates="user")
    staytimes = relationship("Staytime", back_populates="user")

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.login_pwd)

    def hash_password(self, plain_password):
        self.login_pwd = pwd_context.hash(plain_password)


class Outfit(Base):
    __tablename__ = "outfit"

    outfit_id = Column(Integer, primary_key=True, index=True)
    gender = Column(CHAR(2))
    age = Column(Integer(4))
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
    staytimes = relationship("Staytime", back_populates="outfit")
    similars = relationship("Similar", back_populates="outfit")


class Like(Base):
    __tablename__ = "like"

    session_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"), primary_key=True)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="likes")
    outfit = relationship("Outfit", back_populates="likes")


class Click(Base):
    __tablename__ = "click"

    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"), primary_key=True)
    cnt = Column(Integer)
    timestamp = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="clicks")
    outfit = relationship("Outfit", back_populates="clicks")


class Staytime(Base):
    __tablename__ = "staytime"

    user_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"), primary_key=True)
    staytime = Column(Float)

    user = relationship("User", back_populates="staytimes")
    outfit = relationship("Outfit", back_populates="staytimes")


class Similar(Base):
    __tablename__ = "similar"

    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"), primary_key=True)
    similar_outfits = Column(ARRAY(Integer))

    outfit = relationship("Outfit", back_populates="similars")

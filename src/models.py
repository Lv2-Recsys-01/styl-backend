from passlib.context import CryptContext
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, ARRAY
from sqlalchemy.orm import relationship

from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    login_id = Column(String, unique=True, index=True)
    login_pwd = Column(String)

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.login_pwd)

    def hash_password(self, plain_password):
        self.login_pwd = pwd_context.hash(plain_password)


# class User(Base):
#     __tablename__ = "user"

#     user_id = Column(Integer, primary_key=True, index=True)
#     username = Column(String, unique=True, index=True)
#     password = Column(String)


class Outfit(Base):
    __tablename__ = "outfit"

    outfit_id = Column(Integer, primary_key=True, index=True)
    gender = Column(String)
    img_url = Column(String)
    date = Column(DateTime, nullable=False)
    reporter = Column(String)
    style = Column(String)
    origin_url = Column(String)


class Like(Base):
    __tablename__ = "like"

    user_id = Column(Integer, ForeignKey("user.user_id"))
    user = relationship("User")
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"))
    outfit = relationship("Outfit")
    timestamp = Column(DateTime, nullable=False)


class Click(Base):
    __tablename__ = "click"

    user_id = Column(Integer, ForeignKey("user.user_id"))
    user = relationship("User")
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"))
    outfit = relationship("Outfit")
    cnt = Column(Integer)
    timestamp = Column(DateTime, nullable=False)


class Staytime(Base):
    __tablename__ = "staytime"

    user_id = Column(Integer, ForeignKey("user.user_id"))
    user = relationship("User")
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"))
    outfit = relationship("Outfit")
    staytime = Column(Float)

class Similar(Base):
    __tablename__ = "similar"
    
    outfit_id = Column(Integer, ForeignKey("outfit.outfit_id"), primary_key=True)
    outfit = relationship("Outfit")
    similar_outfits = Column(ARRAY(Integer))
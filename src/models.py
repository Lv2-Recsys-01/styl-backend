from sqlalchemy import create_engine, Column, Integer, String, select
from passlib.context import CryptContext
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
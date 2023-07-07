from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from .database import Base  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    login_id = Column(String, unique=True, index=True)
    login_pwd = Column(String)

    likes = relationship("Like", back_populates="users")
    clicks = relationship("Click", back_populates="users")
    sessions = relationship("UserSession", back_populates="users")
    
    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.login_pwd) 

    def hash_password(self, plain_password):
        self.login_pwd = pwd_context.hash(plain_password)
        

class UserSession(Base):
    __tablename__ = "sessions"

    session_id = Column(String, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))

    likes = relationship("Like", back_populates="sessions")
    clicks = relationship("Click", back_populates="sessions")
    users = relationship("User", back_populates="sessions")
    

class Image(Base):
    __tablename__ = "images"
    
    img_id = Column(Integer, primary_key=True, index=True)
    img_url = Column(String, unique=True, index=True)

    likes = relationship("Like", back_populates="images")
    clicks = relationship("Click", back_populates="images")
    

class Click(Base):
    __tablename__ = "clicks"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    img_id = Column(Integer, ForeignKey("images.img_id"), primary_key=True)
    session_id = Column(String, ForeignKey("sessions.session_id"), primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    users = relationship("User", back_populates="clicks")
    images = relationship("Image", back_populates="clicks")
    sessions = relationship("UserSession", back_populates="clicks")
    

class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
    img_id = Column(Integer, ForeignKey("images.img_id"), primary_key=True)
    session_id = Column(String, ForeignKey("sessions.session_id"), primary_key=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="likes")
    images = relationship("Image", back_populates="likes")
    sessions = relationship("UserSession", back_populates="likes")

# from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
# from sqlalchemy.orm import relationship
# from passlib.context import CryptContext
# from .database import Base  

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# class User(Base):
#     __tablename__ = "users"

#     user_id = Column(Integer, primary_key=True, index=True)
#     login_id = Column(String, unique=True, index=True)
#     login_pwd = Column(String)
    
#     def verify_password(self, plain_password):
#         return pwd_context.verify(plain_password, self.login_pwd) # type: ignore

#     def hash_password(self, plain_password):
#         self.login_pwd = pwd_context.hash(plain_password)
        
#     likes = relationship("Like", back_populates="users")
#     clicks = relationship("Click", back_populates="users")
    
    
# class UserSession(Base):
#     __tablename__ = "sessions"

#     session_id = Column(String, primary_key=True)
#     user_id = Column(Integer, ForeignKey("users.user_id"))
    
#     likes = relationship("Like", back_populates="sessions")
#     clicks = relationship("Click", back_populates="sessions")
    
    
# class Image(Base):
#     __tablename__ = "images"
    
#     img_id = Column(Integer, primary_key=True, index=True)
#     img_url = Column(String, unique=True, index=True)
#     # gender = Column(String)
#     # tag = Column(String)
#     # reporter = Column(String)
#     # style = Column(String)
#     # origin_url = Column(String)
#     # date = Column(Date)
    
#     likes = relationship("Like", back_populates="images")
#     clicks = relationship("Click", back_populates="images")
    

# class Click(Base):
#     __tablename__ = "clicks"

#     user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
#     img_id = Column(Integer, ForeignKey("images.img_id"), primary_key=True)
#     session_id = Column(String, ForeignKey("sessions.session_id"), primary_key=True)
#     # timestamp = Column(DateTime)
    
#     users = relationship("User", back_populates="clicks")
#     images = relationship("Image", back_populates="clicks")
#     sessions = relationship("UserSession", back_populates="clicks")
    
    
# class Like(Base):
#     __tablename__ = "likes"

#     user_id = Column(Integer, ForeignKey("users.user_id"), primary_key=True)
#     img_id = Column(Integer, ForeignKey("images.img_id"), primary_key=True)
#     session_id = Column(String, ForeignKey("sessions.session_id"), primary_key=True)
#     # timestamp = Column(DateTime)

#     users = relationship("User", back_populates="likes")
#     images = relationship("Image", back_populates="likes")
#     sessions = relationship("UserSession", back_populates="likes")


    
    
    
from sqlalchemy import create_engine, ARRAY, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DATABASE_URL = "postgresql://postgres:password@localhost:6000/postgres"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, unique=True, index=True)
    user_pwd = Column(String)
    signup_time = Column(DateTime)

    likes = relationship("Like", back_populates="user")
    clicks = relationship("Click", back_populates="user")
    session = relationship("UserSession", back_populates="user")
    mab = relationship("MAB", back_populates="user")


class UserSession(Base):
    __tablename__ = "session"

    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), default=None)
    created_at = Column(DateTime)
    login_at = Column(DateTime, default=None)
    expired_at = Column(DateTime, default=None)

    user = relationship("User", back_populates="session")
    likes = relationship("Like", back_populates="session")
    clicks = relationship("Click", back_populates="session")
    mab = relationship("MAB", back_populates="session")


class MAB(Base):
    __tablename__ = 'mab'

    mab_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.user_id'))
    session_id = Column(String, ForeignKey('session.session_id'))
    alpha = Column(ARRAY(Float))
    beta = Column(ARRAY(Float))

    user = relationship('User', back_populates='mab')
    session = relationship('UserSession', back_populates='mab')


Base.metadata.create_all(bind=engine)

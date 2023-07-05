import random
import string
import time

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, validator
from sqlalchemy import (Column, DateTime, Float, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

SQLALCHEMY_USER_DATABASE_URL = "sqlite:///./test.db"


app = FastAPI()

engine = create_engine(SQLALCHEMY_USER_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


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


class CLick(Base):
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


Base.metadata.create_all(bind=engine)


class UserIn(BaseModel):
    username: str
    password: str
    # confirm_password : str
    @validator("username")
    def username_must_be_more_than_4(cls, v):
        if len(v) <= 4:
            raise ValueError("Username must be more than 4 characters")
        return v

    @validator("password")
    def password_must_be_more_than_4(cls, v):
        if len(v) <= 4:
            raise ValueError("Password must be more than 4 characters")
        return v

    # @validator('confirm_password')
    # def passwords_match(cls, v, values, **kwargs):
    #     if 'password' in values and v != values['password']:
    #         raise ValueError('passwords do not match')
    #     return v


@app.get("/")
async def get_root():
    # return {"root": "Hello World"}
    # 100은 Image DB 의 수
    # 4는 보여줄 이미지 url
    return {"url_num": random.sample([i for i in range(1, 100)], 4)}


# client에 response 보냄
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    with open("../front/login.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


# @app.get("/signup", response_class=HTMLResponse)
# async def signup_form():
#     with open("../front/signup.html", "r", encoding="utf-8") as f:
#         html_content = f.read()
#     return HTMLResponse(content=html_content, status_code=200)


@app.get("/home", response_class=HTMLResponse)
async def signup_form():
    with open("../front/home.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/login")
def login(user: UserIn):
    db = SessionLocal()

    global db_user
    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"id": db_user.id, "username": db_user.username}


@app.post("/signup")
def signup(user: UserIn):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    global db_user

    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"id": db_user.id, "username": db_user.username}


@app.get("/journey")
def journey():
    now = time.time()
    if db_user:
        return {"id": db_user.id, "timestamp": now}
    else:
        db = SessionLocal()
        _length = 50
        string_pool = string.ascii_letters + string.digits
        guest_id, guest_password = "", ""
        for i in range(_length):
            guest_id += random.choice(string_pool)
            guest_password += random.choice(string_pool)

        global db_user

        db_user = User(username=guest_id, password=guest_password)

        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"id": db_user.id, "timestamp": now}


# /journey/?user_id=a1db4ef&outfit_id=1

# @app.on_event('startup')
# def startup_event():
# login url 전송?
# model = model.load(~~)
# Image - 유사 Image DB 로딩 하고 url로 쏴주기?


# @app.get("/image")

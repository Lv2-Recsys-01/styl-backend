from typing import Union

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from sqlalchemy import create_engine, Column, Integer, String, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "*",
]


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@postgres/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    
Base.metadata.create_all(bind=engine)
    
class UserIn(BaseModel):
    username: str
    password: str
    confirm_password: str

    @validator('username')
    def username_check(cls, username: str):
        if not username.isalnum() or len(username) < 4 or len(username) > 20:
            raise ValueError("아이디는 4자리 이상 20자리 이하의 숫자 or 영문자")
        return username
    @validator('password')
    def password_check(cls, password: str):
        if not password.isalnum() or len(password) < 4 or len(password) > 20:
            raise ValueError("비밀번호는 4자리 이상 20자리 이하의 숫자 or 영문자")
        return password
    @validator('confirm_password')
    def passwords_match(cls, confirm_password: str, values: dict):
        if confirm_password and confirm_password != values['password']:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return confirm_password

@app.post("/signup")
def signup(user: UserIn):
    db = SessionLocal()
    
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"id": db_user.id, "username": db_user.username}    
    
@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    result = db.execute(select(User).where(User.id == user_id)).first()
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": result}



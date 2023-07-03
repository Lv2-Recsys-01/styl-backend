from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, ValidationError, validator
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

app = FastAPI()

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

Base.metadata.create_all(bind=engine)

class UserIn(BaseModel):
    username: str
    password: str
    # confirm_password : str
    @validator('username')
    def username_must_be_more_than_4(cls, v):
        if len(v) <= 4:
            raise ValueError('Username must be more than 4 characters')
        return v
    @validator('password')
    def password_must_be_more_than_4(cls, v):
        if len(v) <= 4:
            raise ValueError('Password must be more than 4 characters')
        return v
    # @validator('confirm_password')
    # def passwords_match(cls, v, values, **kwargs):
    #     if 'password' in values and v != values['password']:
    #         raise ValueError('passwords do not match')
    #     return v    

@app.get("/")
async def get_root():
    return {"root": "Hello World"}

# client에 response 보냄
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    with open('../front/login.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/signup", response_class=HTMLResponse)
async def signup_form():
    with open('../front/signup.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/home", response_class=HTMLResponse)
async def signup_form():
    with open('../front/home.html', 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)


@app.post("/login")
def login(user: UserIn):
    db = SessionLocal()

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
    
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"id": db_user.id, "username": db_user.username}


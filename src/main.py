from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .database import engine, Base, get_db
from .schema import UserBase, UserOut, UserSignUp
from .models import User


origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "*"
]
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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

      
@app.post("/login")
def login(user: UserBase, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.login_id == user.login_id).first()
    
    if db_user is None or not pwd_context.verify(user.login_pwd, db_user.login_pwd): # type:ignore
        raise HTTPException(status_code=400, detail="존재하지 않는 아이디이거나 잘못된 비밀번호")

    return {"user_id": db_user.user_id, "login_id": db_user.login_id}

@app.post("/signup")
def signup(user: UserSignUp, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.login_id == user.login_id).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다")
    
    hashed_password = pwd_context.hash(user.login_pwd)
    db_user = User(login_id=user.login_id, login_pwd=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"user_id": db_user.user_id, "login_id": db_user.login_id}    

# @app.get("/users/{user_id}", response_model=UserOut)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     result = db.query(User).filter(User.user_id == user_id).first()
#     if result is None:
#         raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다")
#     return result

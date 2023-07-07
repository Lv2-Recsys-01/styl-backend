from fastapi import FastAPI, HTTPException, Depends, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker
from passlib.context import CryptContext
from typing import List
from .database import engine, Base, get_db
from .schema import UserBase, UserOut, UserSignUp, ImageBase, LikeBase
from .models import User, Image, Like, Click, UserSession
import uuid

from pydantic import BaseModel

# [로그인 없이 사용] 
# 랜덤 uuid(와 같은 식별자)를 프론트 단에서 생성
# -> LS에 저장
# -> 매번 요청시 해당 값을 백단에 넘기기
# -> 백단은 해당 식별자를 가지고 활용

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
    return {"message": "Hello World"}


def merge_likes(session_id: str,
                guest_user_id: int,
                real_user_id: int,
                db: Session):
    # Find the rows to update
    likes = db.query(Like).filter(Like.user_id == guest_user_id, Like.session_id == session_id)

    # Update the rows
    for like in likes:
        like.user_id = real_user_id

    # Commit the changes
    db.commit()
    
 
@app.post("/login")
def login(response: Response,
          user: UserBase = None,
          session_id: str = Cookie(None),
          db: Session = Depends(get_db),
          guest_user_id: int = 1):
    # 회원가입 없이 시작   
    if user is None:
        # guest id 배정
        guest_user = db.query(User).filter(User.user_id == guest_user_id).first()
        # 세션id 생성
        session_id = str(uuid.uuid4())
        # db 저장
        user_session = UserSession(session_id=session_id, user_id=guest_user_id)
        db.add(user_session)
        db.commit()
        db.refresh(user_session)
        # 쿠키 생성
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        response.set_cookie(key='user_id', value=guest_user_id, httponly=True)
        response.set_cookie(key='login_id', value=guest_user.login_id, httponly=True)
        
        return {"message": f"Welcome {guest_user.login_id}",
                "user_id": guest_user_id,
                "login_id": guest_user.login_id,
                "session_id": session_id}
        
    # 유저 로그인
    if user is not None:
        # 로그인 검증
        real_user = db.query(User).filter(User.login_id == user.login_id).first()
        if real_user is None or not pwd_context.verify(user.login_pwd, real_user.login_pwd):
            raise HTTPException(status_code=400, detail="존재하지 않는 아이디이거나 잘못된 비밀번호입니다.")
        
        # 좋아요 병합
        if session_id is not None:
            merge_likes(session_id, guest_user_id, real_user.user_id, db)
        # 세션id 생성
        user_session = UserSession(session_id=session_id, user_id=real_user.user_id)
        # db 저장
        db.add(user_session)
        db.commit()
        db.refresh(user_session)
        # 쿠키 생성
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        response.set_cookie(key='user_id', value=real_user.user_id, httponly=True)
        response.set_cookie(key='login_id', value=real_user.login_id, httponly=True)
        
        return {"message": f"Welcome {user.login_id}",
                "user_id": real_user.user_id,
                "login_id": real_user.login_id,
                "session_id": session_id}


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


@app.post("/upload")
def upload_image(image: ImageBase, db: Session = Depends(get_db)):
    new_img = Image(img_url=image.img_url)
    db.add(new_img)
    db.commit()
    db.refresh(new_img)
    
    return {"message": f"new image {new_img.img_id} from {new_img.img_url} uploaded"}


@app.post("/journey/{img_id}/click")
def user_click(img_id: int,
               user_id: int = Cookie(None),
               session_id: str = Cookie(None),
               db: Session = Depends(get_db)):
    
    new_click = Click(user_id=user_id, img_id=img_id, session_id=session_id)
    db.add(new_click)
    db.commit()
    db.refresh(new_click)
    
    return {"message": f"User {user_id} clicks Image {img_id} at {new_click.timestamp}"}


@app.post("/journey/{img_id}/like")
def user_like(img_id: int,
              user_id: int = Cookie(None),
              session_id: str = Cookie(None),
              db: Session = Depends(get_db)):
    
    new_like = Like(user_id=user_id, img_id=img_id, session_id=session_id)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    return {"message": f"User {user_id} likes Image {img_id} at {new_like.timestamp}"}

@app.get("/likes/{user_id}", response_model=List[LikeBase])
def show_likes(user_id: int,
               session_id: str = Cookie(None),
               db: Session = Depends(get_db)):

    # Find the likes by user_id and session_id
    likes = db.query(Like).filter(Like.user_id == user_id, Like.session_id == session_id).all()

    # If no likes found, return a 404
    if not likes:
        raise HTTPException(status_code=404, detail="Likes not found")

    return likes


# @app.get("/likes/{user_id}")
# def show_likes(user_id: int,
#                session_id: str = Cookie(None),
#                db: Session = Depends(get_db)):
    

# @app.post("/journey")
# def create_click(user_id:int, img_id:int , db: Session = Depends(get_db)):
#     new_click = Like(user_id=user_id, img_id=img_id)
#     db.add(new_click)
#     db.commit()
#     db.refresh(new_click)
#     return {"detail": f"User {user_id} liked Image {img_id}"}

# @app.get("/users/{user_id}", response_model=UserOut)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     result = db.query(User).filter(User.user_id == user_id).first()
#     if result is None:
#         raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다")
#     return result

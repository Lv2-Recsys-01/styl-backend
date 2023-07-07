from fastapi import FastAPI, HTTPException, Depends, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker
from passlib.context import CryptContext
from typing import List
from datetime import datetime
from pytz import timezone
import uuid

from .database import engine, Base, get_db
from .schema import UserBase, UserSignUp, OutfitBase, LikeBase
from .models import User, Outfit, Like, Click, UserSession


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
    guest_likes = db.query(Like).filter(Like.user_id == guest_user_id, Like.session_id == session_id)

    # Update the rows
    for like in guest_likes:
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
        user_session = UserSession(session_id=session_id,
                                   user_id=guest_user_id,
                                   created_at=datetime.now(timezone("Asia/Seoul")),
                                   expired_at=datetime.now(timezone("Asia/Seoul")))
        db.add(user_session)
        db.commit()
        db.refresh(user_session)
        # 쿠키 생성
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        response.set_cookie(key='user_id', value=guest_user_id, httponly=True)
        response.set_cookie(key='user_name', value=guest_user.user_name, httponly=True)
        
        return {"message": f"Welcome {guest_user.user_name}",
                "user_id": guest_user_id,
                "user_name": guest_user.user_name,
                "session_id": session_id}
        
    # 유저 로그인
    if user is not None:
        # 로그인 검증
        real_user = db.query(User).filter(User.user_name == user.user_name).first()
        if real_user is None or not pwd_context.verify(user.user_pwd, real_user.user_pwd):
            raise HTTPException(status_code=400, detail="존재하지 않는 아이디이거나 잘못된 비밀번호입니다.")
        
        # 좋아요 병합
        if session_id is not None:
            merge_likes(session_id, guest_user_id, real_user.user_id, db)
        # 세션id 생성
        session_id = str(uuid.uuid4())
        # db 저장
        user_session = UserSession(session_id=session_id,
                                   user_id=real_user.user_id,
                                   created_at=datetime.now(timezone("Asia/Seoul")),
                                   expired_at=datetime.now(timezone("Asia/Seoul")))
        db.add(user_session)
        db.commit()
        db.refresh(user_session)
        # 쿠키 생성
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        response.set_cookie(key='user_id', value=real_user.user_id, httponly=True)
        response.set_cookie(key='user_name', value=real_user.user_name, httponly=True)
        
        return {"message": f"Welcome {user.user_name}",
                "user_id": real_user.user_id,
                "user_name": real_user.user_name,
                "session_id": session_id}
        
        
@app.post("/logout")
def logout(response: Response,
           user_id: int = Cookie(None),
           session_id: str = Cookie(None),
           db: Session = Depends(get_db)):
    logout_session = db.query(UserSession).filter(UserSession.user_id == user_id,
                                               UserSession.session_id == session_id).first()
    logout_session.expired_at = datetime.now(timezone("Asia/Seoul"))
    
    response.delete_cookie(key='user_id')
    # response.delete_cookie(key='session_id')
    response.delete_cookie(key='user_name')
    
    return {"message": f"User {user_id} logged out at {datetime.now(timezone('Asia/Seoul'))}"}
    


@app.post("/signup")
def signup(user: UserSignUp, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_name == user.user_name).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다")
    
    hashed_password = pwd_context.hash(user.user_pwd)
    db_user = User(user_name=user.user_name, user_pwd=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"user_id": db_user.user_id, "user_name": db_user.user_name}    


@app.post("/upload")
def upload_outfit(outfit: OutfitBase, db: Session = Depends(get_db)):
    new_outfit = Outfit(img_url=outfit.img_url)
    db.add(new_outfit)
    db.commit()
    db.refresh(new_outfit)
    
    return {"message": f"new outfit {new_outfit.outfit_id} from {new_outfit.img_url} uploaded"}


@app.post("/journey/{outfit_id}/click")
def user_click(outfit_id: int,
               user_id: int = Cookie(None),
               session_id: str = Cookie(None),
               db: Session = Depends(get_db)):
    
    new_click = Click(session_id=session_id,
                      user_id=user_id,
                      outfit_id=outfit_id,
                      timestamp=datetime.now(timezone("Asia/Seoul")))
    db.add(new_click)
    db.commit()
    db.refresh(new_click)
    
    return {"message": f"User {user_id} clicks outfit {outfit_id} at {new_click.timestamp}"}


@app.post("/journey/{outfit_id}/like")
def user_like(outfit_id: int,
              user_id: int = Cookie(None),
              session_id: str = Cookie(None),
              db: Session = Depends(get_db)):
    print(user_id)
    print(session_id)
    new_like = Like(session_id=session_id,
                    user_id=user_id,
                    outfit_id=outfit_id,
                    timestamp=datetime.now(timezone("Asia/Seoul")),
                    is_deleted=False)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    
    return {"message": f"User {user_id} likes outfit {outfit_id} at {new_like.timestamp}"}

@app.get("/likes/{user_id}", response_model=List[LikeBase])
def show_likes(user_id: int,
               session_id: str = Cookie(None),
               db: Session = Depends(get_db)):

    # Find the likes by user_id and session_id
    likes = db.query(Like).filter(Like.session_id == session_id,
                                  Like.user_id == user_id,
                                  Like.is_deleted == False).all()

    # If no likes found, return a 404
    if not likes:
        raise HTTPException(status_code=404, detail="Likes not found")

    return likes


# @app.get("/likes/{user_id}")
# def show_likes(user_id: int,
#                session_id: str = Cookie(None),
#                db: Session = Depends(get_db)):
    

# @app.post("/journey")
# def create_click(user_id:int, outfit_id:int , db: Session = Depends(get_db)):
#     new_click = Like(user_id=user_id, outfit_id=outfit_id)
#     db.add(new_click)
#     db.commit()
#     db.refresh(new_click)
#     return {"detail": f"User {user_id} liked Image {outfit_id}"}

# @app.get("/users/{user_id}", response_model=UserOut)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     result = db.query(User).filter(User.user_id == user_id).first()
#     if result is None:
#         raise HTTPException(status_code=404, detail="존재하지 않는 유저입니다")
#     return result

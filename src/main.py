from fastapi import FastAPI, HTTPException, Depends, Request, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session, sessionmaker
from passlib.context import CryptContext
from typing import List
from datetime import datetime
from pytz import timezone
import uuid
import random
import pprint


from .database import engine, Base, get_db
from .schema import UserBase, UserSignUp, OutfitBase, LikeBase, OutfitOut
from .models import User, Outfit, Like, Click, UserSession, Similar
from .router.base import base_router

from pydantic import BaseModel

# [로그인 없이 사용]
# 랜덤 uuid(와 같은 식별자)를 프론트 단에서 생성
# -> LS에 저장
# -> 매번 요청시 해당 값을 백단에 넘기기
# -> 백단은 해당 식별자를 가지고 활용

print = pprint.pprint


# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

app = FastAPI()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,  # True인 경우 allow_origins을 ['*'] 로 설정할 수 없음.
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def handle_user_auth_logic(request: Request, call_next):
    response = await call_next(request)

    # handle user auth logic

    return response


@app.get("/healthz")
def ping_poing():
    return {"ping": "pong!"}


def merge_likes(session_id: str, guest_id: int, real_user_id: int, db: Session):
    # Find the rows to update
    guest_likes = (
        db.query(Like)
        .filter(Like.user_id == guest_id, Like.session_id == session_id)
        .all()
    )

    # Update the rows
    for like in guest_likes:
        like.user_id = real_user_id

    # Commit the changes
    db.commit()


@app.post("/login")
def login(
    response: Response,
    user: UserBase = None,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    # 현재 로그인 된 상태인지 확인
    if user_id != guest_id:
        raise HTTPException(status_code=500, detail="로그아웃을 먼저 하십시오.")
    # 로그인 검증
    login_user = db.query(User).filter(User.user_name == user.user_name).first()
    if login_user is None or not pwd_context.verify(user.user_pwd, login_user.user_pwd):
        raise HTTPException(status_code=500, detail="존재하지 않는 아이디이거나 잘못된 비밀번호입니다.")
    # 좋아요 병합
    merge_likes(session_id, guest_id, login_user.user_id, db)
    # 현재 비회원 세션 만료 표시
    cur_session = (
        db.query(UserSession).filter(UserSession.session_id == session_id).first()
    )
    cur_session.expired_at = datetime.now(timezone("Asia/Seoul"))
    # 새 세션id 생성
    session_id = str(uuid.uuid4())
    # 새 세션 db 저장
    user_session = UserSession(
        session_id=session_id,
        user_id=login_user.user_id,
        created_at=datetime.now(timezone("Asia/Seoul")),
        expired_at=datetime.now(timezone("Asia/Seoul")),
    )
    db.add(user_session)
    db.commit()
    db.refresh(user_session)
    # 쿠키 생성
    response.set_cookie(key="session_id", value=session_id, httponly=True)
    response.set_cookie(key="user_id", value=login_user.user_id, httponly=True)
    response.set_cookie(key="user_name", value=login_user.user_name, httponly=True)

    return {"ok": True, "user_name": login_user.user_name}


@app.post("/logout")
def logout(
    response: Response,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
):
    logout_session = (
        db.query(UserSession)
        .filter(UserSession.user_id == user_id, UserSession.session_id == session_id)
        .first()
    )
    logout_session.expired_at = datetime.now(timezone("Asia/Seoul"))

    response.delete_cookie(key="user_id")
    response.delete_cookie(key="session_id")
    response.delete_cookie(key="user_name")

    return {"ok": True}


@app.post("/signup")
def signup(user: UserSignUp, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.user_name == user.user_name).first()
    if existing_user:
        raise HTTPException(status_code=500, detail="이미 존재하는 아이디입니다")

    hashed_password = pwd_context.hash(user.user_pwd)
    db_user = User(user_name=user.user_name, user_pwd=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"ok": True, "user_name": user.user_name}


# 실험용 임시
@app.post("/upload")
def upload_outfit(outfit: OutfitBase, db: Session = Depends(get_db)):
    new_outfit = Outfit(img_url=outfit.img_url)
    db.add(new_outfit)
    db.commit()
    db.refresh(new_outfit)

    return {
        "message": f"new outfit {new_outfit.outfit_id} from {new_outfit.img_url} uploaded"
    }


@app.get("/journey")
def show_journey_images(
    pagesize: int,
    offset: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    # 한 페이지에 표시할 전체 outfit
    outfits = db.query(Outfit).offset(offset).limit(pagesize).all()
    # 마지막 페이지인지 확인
    is_last = len(outfits) < pagesize

    # 유저가 좋아요 누른 전체 이미지 목록
    # 비회원일때
    if user_id == guest_id:
        likes = (
            db.query(Like)
            .filter(
                Like.user_id == guest_id,
                Like.session_id == session_id,
                Like.is_deleted == False,
            )
            .all()
        )
    # 회원일때
    else:
        likes = (
            db.query(Like)
            .filter(Like.user_id == user_id, Like.is_deleted == False)
            .all()
        )
    # 유저가 좋아요 누른 이미지의 id 집합 생성
    likes_set = {like.outfit_id for like in likes}

    outfits_list = []
    for outfit in outfits:
        # 각 outfit 마다 유저가 좋아요 눌렀는지 확인
        is_liked = outfit.outfit_id in likes_set
        outfit_out = OutfitOut(**outfit.__dict__, is_liked=is_liked)
        outfits_list.append(outfit_out)

    # total_cnt = 64400
    # total_page_count = total_cnt // pagesize + (1 if total_cnt % pagesize else 0)

    return {
        "ok": True,
        "outfits_list": outfits_list,
        "pagesize": pagesize,
        "offset": offset,
        "is_last": is_last,
    }


@app.post("/journey/{outfit_id}/click")
def user_click(
    outfit_id: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
):
    db_outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    if db_outfit is None:
        raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")
    new_click = Click(
        session_id=session_id,
        user_id=user_id,
        outfit_id=outfit_id,
        timestamp=datetime.now(timezone("Asia/Seoul")),
    )
    db.add(new_click)
    db.commit()
    db.refresh(new_click)

    return {"ok": True}


@app.post("/journey/{outfit_id}/like")
def user_like(
    outfit_id: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    db_outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    if db_outfit is None:
        raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")

    # 이전에 좋아요 누른적 있는지 확인
    # 비회원
    if user_id == guest_id:
        already_like = db.query(Like).filter(
            Like.user_id == guest_id,
            Like.session_id == session_id,
            Like.outfit_id == outfit_id,
        )
    # 회원
    else:
        already_like = db.query(Like).filter(
            Like.user_id == user_id, Like.outfit_id == outfit_id
        )
    # 누른적 없으면 DB에 추가
    if not already_like:
        new_like = Like(
            session_id=session_id,
            user_id=user_id,
            outfit_id=outfit_id,
            timestamp=datetime.now(timezone("Asia/Seoul")),
            is_deleted=False,
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
    # 누른적 있으면 취소 여부 바꿔줌
    else:
        already_like.is_delete = ~already_like.is_delete
        db.commit()

    return {"ok": True}


@app.get("/collection")
def show_collection_images(
    pagesize: int,
    offset: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    # 비회원일때
    if user_id == guest_id:
        outfit_ids_list = [
            db.query(Like)
            .filter(
                Like.user_id == guest_id,
                Like.session_id == session_id,
                Like.is_deleted == False,
            )
            .offset(offset)
            .limit(pagesize)
            .all()
        ]
    # 회원일때
    else:
        outfit_ids_list = [
            db.query(Like)
            .filter(Like.user_id == user_id, Like.is_deleted == False)
            .offset(offset)
            .limit(pagesize)
            .all()
        ]

    is_last = len(outfit_ids_list) < pagesize

    if not outfit_ids_list:
        raise HTTPException(status_code=500, detail="좋아요한 사진이 없습니다.")

    outfits_list = list()
    for outfit_id in outfit_ids_list:
        outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id)
        outfit_out = OutfitOut(**outfit.__dict__, is_liked=True)
        outfits_list.append(outfit_out)

    return {
        "ok": True,
        "outfits_list": outfits_list,
        "pagesize": pagesize,
        "offset": offset,
        "is_last": is_last,
    }


@app.get("/journey/{outfit_id}")
def show_single_image(
    outfit_id: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    if outfit is None:
        raise HTTPException(status_code=500, detail="Outfit not found")

    # 좋아요 눌렀는지 체크
    # 비회원
    if user_id == guest_id:
        user_like = db.query(Like).filter(
            Like.user_id == guest_id,
            Like.session_id == session_id,
            Like.outfit_id == outfit_id,
            Like.is_deleted == False,
        )
    # 회원
    else:
        user_like = db.query(Like).filter(
            Like.user_id == user_id,
            Like.outfit_id == outfit_id,
            Like.is_deleted == False,
        )
    # is_liked : user_like 존재하면 True, 아니면 False
    is_liked = user_like is not None
    outfit_out = OutfitOut(**outfit.__dict__, is_liked=is_liked)

    similar_outfits = db.query(Similar).filter(Similar.outfit_id == outfit_id).first()
    if similar_outfits is None:
        raise HTTPException(status_code=500, detail="Similar outfits not found")

    similar_outfits_list = list()
    for similar_outfit_id in similar_outfits:
        similar_outfit = (
            db.query(Outfit).filter(Outfit.outfit_id == similar_outfit_id).first()
        )
        if similar_outfit is None:
            raise HTTPException(
                status_code=500, detail="Id for this similar outfit not found"
            )
        # 좋아요 눌렀는지 체크
        # 비회원
        if user_id == guest_id:
            user_like = db.query(Like).filter(
                Like.user_id == guest_id,
                Like.session_id == session_id,
                Like.outfit_id == similar_outfit_id,
                Like.is_deleted == False,
            )
        # 회원
        else:
            user_like = db.query(Like).filter(
                Like.user_id == user_id,
                Like.outfit_id == similar_outfit_id,
                Like.is_deleted == False,
            )
        # is_liked : user_like 존재하면 True, 아니면 False
        is_liked = user_like is not None
        similar_outfit_out = OutfitOut(**similar_outfit.__dict__, is_liked=is_liked)
        similar_outfits_list.append(similar_outfit_out)

    return {
        "ok": True,
        "outfit": outfit_out,
        "similar_outfits_list": similar_outfits_list,
    }

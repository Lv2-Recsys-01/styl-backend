import uuid
from datetime import datetime
from typing import Annotated

from fastapi import (APIRouter, Body, Cookie, Depends, HTTPException, Response,
                     status)
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from pytz import timezone
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Like, User
from ..schema import UserBase, UserSignUp

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


from fastapi.responses import JSONResponse


@router.post("/login")
def login(
    user_body: Annotated[UserBase | None, Body()] = None,
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    if user_body is None or user_body.user_name is None or user_body.user_pwd is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그인 정보가 없습니다.",
        )

    if user_id is not None:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail="이미 로그인 되어 있습니다",
        )

    login_user = db.query(User).filter(User.user_name == user_body.user_name).first()

    if login_user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="존재하지 않는 아이디 입니다.",
        )

    # if pwd_context.verify(user_body.user_pwd, login_user.user_pwd):
    #     raise HTTPException(status_code=500, detail="존재하지 않는 아이디이거나 잘못된 비밀번호입니다.")
    # # 좋아요 병합
    # merge_likes(session_id, guest_id, login_user.user_id, db)
    # # 현재 비회원 세션 만료 표시
    # cur_session = (
    #     db.query(UserSession).filter(UserSession.session_id == session_id).first()
    # )
    # cur_session.expired_at = datetime.now(timezone("Asia/Seoul"))
    # # 새 세션id 생성
    # session_id = str(uuid.uuid4())
    # # 새 세션 db 저장
    # user_session = UserSession(
    #     session_id=session_id,
    #     user_id=login_user.user_id,
    #     created_at=datetime.now(timezone("Asia/Seoul")),
    #     expired_at=datetime.now(timezone("Asia/Seoul")),
    # )
    # db.add(user_session)
    # db.commit()
    # db.refresh(user_session)
    # # 쿠키 생성
    # response.set_cookie(key="session_id", value=session_id, httponly=True)
    # response.set_cookie(key="user_id", value=login_user.user_id, httponly=True)
    # response.set_cookie(key="user_name", value=login_user.user_name, httponly=True)

    # return {"ok": True, "user_name": login_user.user_name}


@router.post("/logout")
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


@router.post("/signup")
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
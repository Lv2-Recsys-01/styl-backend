import uuid
import numpy as np
from datetime import datetime
from typing import Annotated

from fastapi import (APIRouter, Body, Cookie, Depends, HTTPException, Response,
                     status)
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from pytz import timezone
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Like, User, UserSession, MAB
from ..schema import UserBase, UserSignUp

from .mab import get_mab_model


router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/login")
def login(
    response: Response,
    user_body: Annotated[UserBase | None, Body()] = None,
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
) -> dict:
    if user_body is None or user_body.user_name is None or user_body.user_pwd is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그인 정보가 없습니다.",
        )

    if user_id is not None:
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            detail="이미 로그인 되어 있습니다.",
        )

    login_user = db.query(User).filter(User.user_name == user_body.user_name).first()

    if login_user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="존재하지 않는 아이디입니다.",
        )

    if not pwd_context.verify(user_body.user_pwd, str(login_user.user_pwd)):
        raise HTTPException(status_code=500, detail="비밀번호 검증에 실패했습니다.")

    response.set_cookie(key="user_id", value=str(login_user.user_id))
    response.set_cookie(key="user_name", value=str(login_user.user_name))

    # 비회원 세션의 Like에 user_id 삽입 & 중복 제거
    guest_likes = (
        db.query(Like)
        .filter(Like.user_id.is_(None), Like.session_id == session_id)
        .all()
    )

    login_user_likes = (
        db.query(Like)
        .filter(Like.user_id == login_user.user_id)
        .all()
    )

    login_user_likes_outfit_id = {like.outfit_id for like in login_user_likes}

    for like in guest_likes:
        if like.outfit_id not in login_user_likes_outfit_id:
            like.user_id = login_user.user_id
            
    # 알파 베타 추가
    guest_mab = (
        db.query(MAB)
        .filter(MAB.user_id.is_(None), MAB.session_id == session_id)
        .first()
    )
    if guest_mab:
        guest_alpha = guest_mab.alpha
        guest_beta = guest_mab.beta
    else:
        guest_alpha = [0] * 200
        guest_beta = [0] * 200
    
    user_mab_model = get_mab_model(user_id=user_id, session_id=None, db=db)
    user_mab_model.alpha = user_mab_model.alpha + np.array(guest_alpha)
    user_mab_model.beta = user_mab_model.beta + np.array(guest_beta)
    user_mab = db.query(MAB).filter(MAB.user_id == user_id,
                                    MAB.session_id.is_(None)).first()
    
    user_mab.alpha = user_mab_model.alpha.tolist()
    user_mab.beta = user_mab_model.beta.tolist()

    # 현재 비회원 세션에 user_id 추가하기
    cur_session: UserSession | None = (
        db.query(UserSession).filter(UserSession.session_id == session_id).first()
    )
    if cur_session and cur_session.user_id is None:
        # type: ignore
        cur_session.user_id = int(login_user.user_id)  # type: ignore
        cur_session.login_at = datetime.now(timezone("Asia/Seoul")) #type: ignore

    db.commit()
    
    return {"ok": True, "user_id": login_user.user_id, "user_name": login_user.user_name}


@router.post("/signup")
def signup(
    user_body: Annotated[UserSignUp | None, Body()] = None,
    db: Session = Depends(get_db),
) -> dict:
    if user_body is None or user_body.user_name is None or user_body.user_pwd is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="회원가입 정보가 없습니다.",
        )

    existed_user = db.query(User).filter(User.user_name == user_body.user_name).first()
    if existed_user:
        raise HTTPException(status_code=500, detail="이미 존재하는 아이디입니다.")

    hashed_password = pwd_context.hash(user_body.user_pwd)
    db_user = User(user_name=user_body.user_name,
                   user_pwd=hashed_password,
                   signup_time=datetime.now(timezone("Asia/Seoul")))
    db.add(db_user)
    db.commit()

    return {"ok": True, "user_name": db_user.user_name}


@router.post("/logout")
def logout(
    response: Response,
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
) -> dict:
    logout_session: UserSession | None = (
        db.query(UserSession)
        .filter(
            UserSession.session_id == session_id,
            UserSession.user_id == user_id,
        )
        .first()
    )

    if logout_session:
        # type: ignore
        logout_session.expired_at = datetime.now(timezone("Asia/Seoul"))  # type: ignore
        db.commit()

    response.delete_cookie(key="user_id")
    response.delete_cookie(key="session_id")
    response.delete_cookie(key="user_name")

    return {"ok": True}

import uuid
from datetime import datetime

from fastapi import APIRouter, Cookie, Depends, Response
from pytz import timezone
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, UserSession

base_router = APIRouter()


def get_or_create_session_id(response: Response, session_id: str = Cookie(None)):
    if session_id is None:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    return session_id


@base_router.get("/")
def base_path(
    response: Response,
    session_id: str = Depends(get_or_create_session_id),
    user_id: int = Cookie(None),
    db: Session = Depends(get_db),
    guest_user_id: int = 1,
):
    if user_id is None:
        # guest id, name 배정
        guest_user = db.query(User).filter(User.user_id == guest_user_id).first()
        guest_user_name = guest_user.user_name
        # db 저장
        user_session = UserSession(
            session_id=session_id,
            user_id=guest_user_id,
            created_at=datetime.now(timezone("Asia/Seoul")),
            expired_at=datetime.now(timezone("Asia/Seoul")),
        )
        db.add(user_session)
        db.commit()
        db.refresh(user_session)
        # 쿠키 생성
        response.set_cookie(key="user_id", value=guest_user_id, httponly=True)
        response.set_cookie(key="user_name", value=guest_user_name, httponly=True)

import pprint
import uuid
from datetime import datetime
from typing import Annotated

from fastapi import Cookie, Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from pytz import timezone
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import UserSession
from .router import item_router, user_router

print = pprint.pprint

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def create_session_id_first_visit(
    response: Response,
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
):
    if session_id is None:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id)

        user_session = UserSession(
            session_id=session_id,
            user_id=user_id if user_id else None,
            created_at=datetime.now(timezone("Asia/Seoul")),
        )  # type: ignore

        db.add(user_session)
        db.commit()

    return session_id


app = FastAPI(
    description="Outfit Recommendation API",
    version="0.1.0",
    title="Outfit Recommendation API",
    dependencies=[Depends(create_session_id_first_visit)],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_origin_regex="https://.*\.ngrok\-free\.app",
    allow_credentials=True,  # True인 경우 allow_origins을 ['*'] 로 설정할 수 없음.
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def handle_user_auth_logic(
    request: Request,
    call_next,
):
    # in case of using request directly,
    # https://www.starlette.io/requests/

    response = await call_next(request)

    # response examples
    response.set_cookie("temp_cookie", "temp_cookie_value")
    response.headers["X-Custom-Header"] = "Custom Value"

    return response


@app.get("/healthz")
def ping_poing():
    return {"ping": "pong!"}


@app.get("/drop_all")
def drop_all_db():
    Base.metadata.drop_all(bind=engine)
    return {"drop": "all"}


app.include_router(user_router.router)
app.include_router(item_router.router)

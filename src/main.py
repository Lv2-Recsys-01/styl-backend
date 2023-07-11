import pprint

from fastapi import Cookie, Depends, FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Outfit
from .router import item_router, user_router
from .schema import OutfitBase

# [로그인 없이 사용]
# 랜덤 uuid(와 같은 식별자)를 프론트 단에서 생성
# -> LS에 저장
# -> 매번 요청시 해당 값을 백단에 넘기기
# -> 백단은 해당 식별자를 가지고 활용

print = pprint.pprint

Base.metadata.create_all(bind=engine)

app = FastAPI(
    description="Outfit Recommendation API",
    version="0.1.0",
    title="Outfit Recommendation API",
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


def get_or_create_session_id(response: Response, session_id: str = Cookie(None)):
    if session_id is None:
        session_id = str(uuid.uuid4())
        response.set_cookie(key="session_id", value=session_id, httponly=True)
    return session_id


@app.middleware("http")
async def handle_user_auth_logic(
    request: Request,
    call_next,
):
    # in case of using request directly,
    # https://www.starlette.io/requests/

    response = await call_next(request)

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

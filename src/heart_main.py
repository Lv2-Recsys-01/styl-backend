from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .database import engine, Base, get_db
from .schema import UserBase, UserOut, UserSignUp
from .models import User, Outfit, Like, Click, Staytime, Similar


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

@app.post("/heart")
def heart(user_id: int, outfit_id: int, db: Session = Depends(get_db)):
    existing_heart = db.query(Like).filter(Like.user_id == user_id, Like.outfit_id == outfit_id).first()
    if existing_heart:
        db.delete(existing_heart)
        db.commit()
        return {"ok": True}
    else:
        new_heart = Like(user_id=user_id, outfit_id=outfit_id)
        db.add(new_heart)
        db.commit()
        return {"ok": True}


# 요렇게 하면 PUT Method가 필요 없을지도?
# 만약 한 API에는 한 기능만 들어가야 하면 죄송합니다..
# 만약 return으로 outfit_id를 보내면 front 단에서 편하려나요? (잘 모르겠습니다)

@app.get("/heart")
async def heart(user_id: int, pagesize: int, offset: int, db: Session = Depends(get_db)):
    outfits = db.query(Like).filter(Like.user_id == user_id).all()
    total_page_count = len(outfits) // pagesize
    try:
        outfits = outfits[offset:offset+pagesize]
        is_last = True
    except:
        outfits = outfits[offset:]
        is_last = False

    return {"outfits": outfits, "pagesize": pagesize, "offset": offset,"is_last": is_last,"total_page_count": total_page_count}


# 제가 SQL 언어를 잘 몰라서 시간대별로 내림차순하는 거랑 indexing 하는 코드가 맞는지 살펴봐 주시면 감사하겠습니다 ..
# 현재 도커가 먹통이라 실험을 못해봤습니다 ㅠㅡㅠ

@app.get("/images")
async def images(user_id: int, pagesize: int, offset: int, db: Session = Depends(get_db)):
    outfits = db.query(Outfit).filter(Outfit.user_id == user_id).all()
    total_page_count = len(outfits) // pagesize
    try:
        outfits = outfits[offset:offset+pagesize]
        is_last = True
    except:
        outfits = outfits[offset:]
        is_last = False

    like_added_outfits = []
    for outfit in outfits:
        try:
            is_liked = db.query(Like).filter(Like.user_id == user_id, Like.outfit_id == outfit.outfit_id).first()
            outfit.update({"is_liked": True})
        except:
            outfit.update({"is_liked": False})

        like_added_outfits.append(outfit)

    return {"outfits": like_added_outfits, "pagesize": pagesize, "offset": offset,"is_last": is_last,"total_page_count": total_page_count}

# 코드가 실행되지 않을 가능성 다분합니다! 이런 로직으로 구현 되면 되지 않을까 해서 만들었슴다


@app.get("/image")
async def image(user_id: int, outfit_id: int, db: Session = Depends(get_db)):
    outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    try:
        is_liked = db.query(Like).filter(Like.user_id == user_id, Like.outfit_id == outfit.outfit_id).first()
        outfit.update({"is_liked": True})
    except:
        outfit.update({"is_liked": False})
    similar_outfits = db.query(Similar).filter(Similar.outfit_id == outfit_id).all()
    url_added_similar_outfits = []

    for similar_outfit in similar_outfits:
        img_url = db.query(Outfit).filter(Outfit.outfit_id == similar_outfit).first().img_url
        similar_outfit.update({"img_url": img_url})
        url_added_similar_outfits.append(similar_outfit)


    return {"outfit": outfit, 'similar_outfits': url_added_similar_outfits}

# readme api 명세에 pagesize랑 offset, is_last가 있는데, 단 건이라 필요 없지 않나요?
# 모델 만들기 전까지 Similar 이라는 Table을 추가로 만들어 땡겨오는 방식으로 사용해야 할 것 같습니다!

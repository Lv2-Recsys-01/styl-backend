from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .database import engine, Base, get_db
from .schema import UserBase, UserOut, UserSignUp
from .models import User, Outfit, Like, Click, Staytime


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
async def heart(user_id: int, page_size: int, offset: int, db: Session = Depends(get_db)):
    outfits = db.query(Like).filter(Like.user_id == user_id).all()
    try:
        outfits = outfits[offset:offset+page_size]
        is_last = True
    except:
        outfits = outfits[offset:]
        is_last = False
    
    return {"outfits": outfits, "pagesize": page_size, "offset": offset,"is_last": is_last}
    
    
# 제가 SQL 언어를 잘 몰라서 시간대별로 내림차순하는 거랑 indexing 하는 코드가 맞는지 살펴봐 주시면 감사하겠습니다 .. 
# 현재 도커가 먹통이라 실험을 못해봤습니다 ㅠㅡㅠ 




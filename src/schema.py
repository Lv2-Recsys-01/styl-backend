from datetime import datetime
from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, validator


class UserBase(BaseModel):
    user_name: str
    user_pwd: str

    @validator("user_name")
    def login_id_check(cls, user_name: str):
        if not user_name.isalnum() or len(user_name) < 4 or len(user_name) > 20:
            raise HTTPException(
                status_code=500, detail="아이디는 4자리 이상 20자리 이하의 숫자 or 영문자"
            )
        return user_name

    @validator("user_pwd")
    def login_pwd_check(cls, user_pwd: str):
        if not user_pwd.isalnum() or len(user_pwd) < 4 or len(user_pwd) > 20:
            raise HTTPException(
                status_code=500, detail="비밀번호는 4자리 이상 20자리 이하의 숫자 or 영문자"
            )
        return user_pwd


class UserSignUp(UserBase):
    confirm_pwd: str

    @validator("confirm_pwd")
    def passwords_match(cls, confirm_pwd: str, values: dict):
        if confirm_pwd and confirm_pwd != values["user_pwd"]:
            raise HTTPException(status_code=500, detail="비밀번호가 일치하지 않습니다")
        return confirm_pwd


class OutfitBase(BaseModel):
    img_url: str


class LikeBase(BaseModel):
    user_id: int
    outfit_id: int
    session_id: str
    timestamp: datetime

    class Config:
        orm_mode = True


class ClickBase(BaseModel):
    user_id: int
    img_id: int
    session_id: str
    timestamp: datetime

    class Config:
        orm_mode = True


class OutfitOut(BaseModel):
    outfit_id: int
    img_url: str
    gender: str
    age: int
    origin_url: str
    reporter: str
    tags: List[str]
    brands: List[str]
    region: str
    occupation: str
    style: str
    date: datetime
    is_liked: bool

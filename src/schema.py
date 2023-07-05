from pydantic import BaseModel, validator

class UserBase(BaseModel):
    login_id: str
    login_pwd: str

    @validator('login_id')
    def login_id_check(cls, login_id: str):
        if not login_id.isalnum() or len(login_id) < 4 or len(login_id) > 20:
            raise ValueError("아이디는 4자리 이상 20자리 이하의 숫자 or 영문자")
        return login_id
    @validator('login_pwd')
    def login_pwd_check(cls, login_pwd: str):
        if not login_pwd.isalnum() or len(login_pwd) < 4 or len(login_pwd) > 20:
            raise ValueError("비밀번호는 4자리 이상 20자리 이하의 숫자 or 영문자")
        return login_pwd


class UserSignUp(UserBase):
    confirm_pwd: str

    @validator('confirm_pwd')
    def passwords_match(cls, confirm_pwd: str, values: dict):
        if confirm_pwd and confirm_pwd != values['login_pwd']:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return confirm_pwd    
    
    
class UserOut(UserBase):
    user_id: int

    class Config:
        orm_mode = True



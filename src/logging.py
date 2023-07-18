import os
from datetime import datetime
from pytz import timezone
from sqlalchemy.orm import Session
from .models import UserSession


async def update_last_action_time(user_id: int | None,
                                  session_id: str,
                                  db: Session):
    if user_id is None:
        user = db.query(UserSession).filter(
            UserSession.session_id == session_id,
            UserSession.user_id.is_(None),
        ).first()
    else:
        user = db.query(UserSession).filter(
            UserSession.session_id == session_id,
            UserSession.user_id == user_id,
        ).first()
    
    user.expired_at = datetime.now(timezone("Asia/Seoul")) # type: ignore

    db.commit()
    

async def log_view_image(user_id: int | None,
                         session_id: str,
                         outfits_list: list,
                         view_type: str):
    if user_id is None:
        user_id = 0
    timestamp = str(datetime.now(timezone("Asia/Seoul")).strftime("%y-%m-%d %H:%M:%S"))
    os.makedirs(name="./logging", exist_ok=True)
    file_path = "./logging/view_image_log.txt"

    if not os.path.exists(file_path):
        with open(file_path, "w") as log_file:
            log_file.write("session_id,user_id,outfit_id,timestamp,view_type\n")
            
    with open(file_path, "a") as log_file:
        for outfit_out in outfits_list:
            log_entry = f"{session_id},{user_id},{outfit_out.outfit_id},{timestamp},{view_type}\n"
            log_file.write(log_entry)
            
            
async def log_click_image(user_id: int | None,
                         session_id: str,
                         outfit_id: int,
                         click_type: str | None = None):
    if user_id is None:
        user_id = 0
    timestamp = str(datetime.now(timezone("Asia/Seoul")).strftime("%y-%m-%d %H:%M:%S"))
    os.makedirs(name="./logging", exist_ok=True)
    file_path = "./logging/click_image_log.txt"

    if not os.path.exists(file_path):
        with open(file_path, "w") as log_file:
            log_file.write("session_id,user_id,outfit_id,timestamp,click_type\n")
            
    with open(file_path, "a") as log_file:
        log_entry = f"{session_id},{user_id},{outfit_id},{timestamp},{click_type}\n"
        log_file.write(log_entry)


async def log_click_share_musinsa(session_id: str,
                                  user_id: int | None,
                                  outfit_id: int,
                                  click_type: str):
    if user_id is None:
        user_id = 0
    timestamp = str(datetime.now(timezone("Asia/Seoul")).strftime("%y-%m-%d %H:%M:%S"))
    os.makedirs(name="./logging", exist_ok=True)
    file_path = "./logging/click_share_musinsa_log.txt"
    
    if not os.path.exists(file_path):
        with open(file_path, "w") as log_file:
            log_file.write("session_id,user_id,outfit_id,timestamp,click_type\n")
    
    with open(file_path, "a") as log_file:
        log_entry = f"{session_id},{user_id},{outfit_id},{timestamp},{click_type}\n"
        log_file.write(log_entry)



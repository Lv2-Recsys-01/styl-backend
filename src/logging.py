import os
from datetime import datetime

from pytz import timezone
from sqlalchemy.orm import Session

from .models import UserSession


async def update_last_action_time(user_id: int | None, session_id: str, db: Session):
    if user_id is None:
        user = (
            db.query(UserSession)
            .filter(
                UserSession.session_id == session_id,
                UserSession.user_id.is_(None),
            )
            .first()
        )
    else:
        user = (
            db.query(UserSession)
            .filter(
                UserSession.session_id == session_id,
                UserSession.user_id == user_id,
            )
            .first()
        )

    if user:
        user.expired_at = datetime.now(timezone("Asia/Seoul"))  # type: ignore

    db.commit()


async def log_view_image(
    user_id: int | None,
    session_id: str,
    outfits_list: list,
    view_type: str,
    bucket: str | None = None,
):
    logs_dir = "./logging"
    os.makedirs(logs_dir, exist_ok=True)
    date_dir = os.path.join(logs_dir, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(date_dir, exist_ok=True)
    if bucket is None:
        bucket = "none"
        file_path = os.path.join(date_dir, "view_image_log.txt")
    else:
        file_path = os.path.join(date_dir, "view_image_log_ab-test.txt")

    if user_id is None:
        user_id = 0
    timestamp = str(datetime.now(timezone("Asia/Seoul")).strftime("%y-%m-%d %H:%M:%S"))

    if not os.path.exists(file_path):
        with open(file_path, "w") as log_file:
            log_file.write("session_id,user_id,outfit_id,timestamp,view_type,bucket\n")

    with open(file_path, "a") as log_file:
        for outfit_out in outfits_list:
            log_entry = f"{session_id},{user_id},{outfit_out.outfit_id},{timestamp},{view_type},{bucket}\n"
            log_file.write(log_entry)


async def log_click_image(
    user_id: int | None,
    session_id: str,
    outfit_id: int,
    click_type: str | None = None,
    bucket: str | None = None,
):
    logs_dir = "./logging"
    os.makedirs(logs_dir, exist_ok=True)
    date_dir = os.path.join(logs_dir, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(date_dir, exist_ok=True)
    if bucket is None:
        bucket = "none"
        file_path = os.path.join(date_dir, "click_image_log.txt")
    else:
        file_path = os.path.join(date_dir, "click_image_log_ab-test.txt")

    if user_id is None:
        user_id = 0
    timestamp = str(datetime.now(timezone("Asia/Seoul")).strftime("%y-%m-%d %H:%M:%S"))

    if not os.path.exists(file_path):
        with open(file_path, "w") as log_file:
            log_file.write("session_id,user_id,outfit_id,timestamp,click_type,bucket\n")

    with open(file_path, "a") as log_file:
        log_entry = (
            f"{session_id},{user_id},{outfit_id},{timestamp},{click_type},{bucket}\n"
        )
        log_file.write(log_entry)


async def log_click_share_musinsa(
    session_id: str,
    user_id: int | None,
    outfit_id: int,
    click_type: str,
    bucket: str | None = None,
):
    logs_dir = "./logging"
    os.makedirs(logs_dir, exist_ok=True)
    date_dir = os.path.join(logs_dir, datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(date_dir, exist_ok=True)
    if bucket is None:
        bucket = "none"
        file_path = os.path.join(date_dir, "click_share_musinsa_log.txt")
    else:
        file_path = os.path.join(date_dir, "click_share_musinsa_log_ab-test.txt")

    if user_id is None:
        user_id = 0
    timestamp = str(datetime.now(timezone("Asia/Seoul")).strftime("%y-%m-%d %H:%M:%S"))

    if not os.path.exists(file_path):
        with open(file_path, "w") as log_file:
            log_file.write("session_id,user_id,outfit_id,timestamp,click_type,bucket\n")

    with open(file_path, "a") as log_file:
        log_entry = (
            f"{session_id},{user_id},{outfit_id},{timestamp},{click_type},{bucket}\n"
        )
        log_file.write(log_entry)

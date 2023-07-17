import random
from datetime import datetime
from typing import Annotated

from fastapi import (APIRouter, Cookie, Depends, HTTPException, Path, Query,
                     status)
from pytz import timezone
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Click, Like, Outfit, Similar
from ..schema import OutfitOut

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get("/journey")
def show_journey_images(
    page_size: Annotated[int, Query()],
    offset: Annotated[int, Query()],
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
) -> dict:

    # 한 페이지에 표시할 전체 outfit
    # outfits = (
    #     db.query(Outfit).order_by(func.random()).offset(offset).limit(page_size).all()
    # )


    f_outfits = (
        db.query(Outfit)
        .filter(Outfit.gender == 'F')
        .order_by(func.random())
        .limit(page_size // 2)
        .all()
    )

    m_outfits = (
        db.query(Outfit)
        .filter(Outfit.gender == 'M')
        .order_by(func.random())
        .limit(page_size // 2)
        .all()
    )

    outfits = f_outfits + m_outfits
    random.shuffle(outfits)

    # 마지막 페이지인지 확인
    if page_size % 2 ==1:
        is_last = len(outfits) < page_size-1
    else:
        is_last = len(outfits) < page_size

    # 유저가 좋아요 누른 전체 이미지 목록
    # 비회원일때
    if user_id is None and session_id is not None:
        likes = (
            db.query(Like)
            .filter(
                Like.session_id == session_id,
                Like.user_id.is_(None),
                Like.is_deleted == bool(False),
            )
            .all()
        )
    # 회원일때
    else:
        likes = (
            db.query(Like)
            .filter(
                Like.user_id == user_id,
                Like.is_deleted == bool(False),
            )
            .all()
        )

    # 유저가 좋아요 누른 이미지의 id 집합 생성
    likes_set = {like.outfit_id for like in likes}

    outfits_list = []

    for outfit in outfits:
        # 각 outfit 마다 유저가 좋아요 눌렀는지 확인
        is_liked = outfit.outfit_id in likes_set
        outfit_out = OutfitOut(**outfit.__dict__, is_liked=is_liked)
        outfits_list.append(outfit_out)

    return {
        "ok": True,
        "outfits_list": outfits_list,
        "page_size": page_size,
        "offset": offset,
        "is_last": is_last,
    }


@router.get("/collection")
def show_collection_images(
    page_size: Annotated[int, Query()],
    offset: Annotated[int, Query()],
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
):
    # 비회원일때
    if user_id is None and session_id is not None:
        liked_list = (
            db.query(Like)
            .filter(
                Like.session_id == session_id,
                Like.user_id.is_(None),
                Like.is_deleted == bool(False),
            )
            .offset(offset)
            .limit(page_size+1)
            .all()
        )
    # 회원일때
    else:
        liked_list = (
            db.query(Like)
            .filter(
                Like.user_id == user_id,
                Like.is_deleted == bool(False),
            )
            .offset(offset)
            .limit(page_size+1)
            .all()
        )
    is_last = len(liked_list) <= page_size
    if len(liked_list) == page_size+1:
        liked_list.pop()

    if len(liked_list) == 0 or not liked_list:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="좋아요한 사진이 없습니다.",
        )

    outfits_list = list()
    for liked in liked_list:
        liked_outfit = (
            db.query(Outfit).filter(Outfit.outfit_id == liked.outfit_id).first()
        )
        outfit_out = OutfitOut(**liked_outfit.__dict__, is_liked=True)
        outfits_list.append(outfit_out)

    return {
        "ok": True,
        "outfits_list": outfits_list,
        "page_size": page_size,
        "offset": offset,
        "is_last": is_last,
    }


@router.post("/journey/{outfit_id}/like")
def user_like(
    outfit_id: Annotated[int, Path()],
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
):
    db_outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    if db_outfit is None:
        raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")

    # 이전에 좋아요 누른적 있는지 확인
    # 비회원
    if user_id is None and session_id is not None:
        already_like: Like = (
            db.query(Like)
            .filter(
                Like.user_id.is_(None),
                Like.session_id == session_id,
                Like.outfit_id == outfit_id,
            )
            .first()
        )
    # 회원
    else:
        already_like = (
            db.query(Like)
            .filter(
                Like.user_id == user_id,
                Like.outfit_id == outfit_id,
            )
            .first()
        )
    # 누른적 없으면 DB에 추가
    if not already_like:
        new_like = Like(
            session_id=session_id,
            user_id=user_id,
            outfit_id=outfit_id,
            timestamp=datetime.now(timezone("Asia/Seoul")),
        )
        db.add(new_like)
        db.commit()
        return {"ok": True}
    # 누른적 있으면 취소 여부 바꿔줌
    else:
        already_like.is_deleted = not bool(already_like.is_deleted)  # type: ignore
        db.commit()
        return {"ok": True}


@router.get("/journey/{outfit_id}")
def show_single_image(
    outfit_id: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
):
    outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    if outfit is None:
        raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")

    # 좋아요 눌렀는지 체크
    # 비회원
    if user_id is None:
        user_like = (
            db.query(Like)
            .filter(
                Like.session_id == session_id,
                Like.user_id.is_(None),
                Like.outfit_id == outfit_id,
                Like.is_deleted == bool(False),
            )
            .first()
        )
    # 회원
    else:
        user_like = (
            db.query(Like)
            .filter(
                Like.user_id == user_id,
                Like.outfit_id == outfit_id,
                Like.is_deleted == bool(False),
            )
            .first()
        )

    # is_liked : user_like 존재하면 True, 아니면 False
    is_liked = user_like is not None
    outfit_out = OutfitOut(**outfit.__dict__, is_liked=is_liked)

    similar_outfits = db.query(Similar).filter(Similar.outfit_id == outfit_id).first()

    if similar_outfits is None:
        raise HTTPException(status_code=500, detail="유사 코디 이미지가 존재하지 않습니다.")

    sampled_k = 3
    sampled_similar_outfits = random.sample(similar_outfits.similar_outfits, sampled_k)

    similar_outfits_list = list()

    for similar_outfit_id in sampled_similar_outfits:
        similar_outfit = (
            db.query(Outfit).filter(Outfit.outfit_id == similar_outfit_id).first()
        )
        if similar_outfit is None:
            raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")
        # 좋아요 눌렀는지 체크
        # 비회원
        if user_id is None and session_id is not None:
            user_like = (
                db.query(Like)
                .filter(
                    Like.session_id == session_id,
                    Like.outfit_id == similar_outfit_id,
                    Like.is_deleted == bool(False),
                )
                .first()
            )
        # 회원
        else:
            user_like = (
                db.query(Like)
                .filter(
                    Like.user_id == user_id,
                    Like.outfit_id == similar_outfit_id,
                    Like.is_deleted == bool(False),
                )
                .first()
            )
        # is_liked : user_like 존재하면 True, 아니면 False
        is_liked = user_like is not None
        similar_outfit_out = OutfitOut(**similar_outfit.__dict__, is_liked=is_liked)
        similar_outfits_list.append(similar_outfit_out)

    return {
        "ok": True,
        "outfit": outfit_out,
        "similar_outfits_list": similar_outfits_list,
    }


@router.post("/journey/{outfit_id}/click")
def user_click(
    outfit_id: Annotated[int, Path()],
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
):
    db_outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()

    if db_outfit is None:
        raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")

    new_click = Click(
        session_id=session_id,
        user_id=user_id,
        outfit_id=outfit_id,
        timestamp=datetime.now(timezone("Asia/Seoul")),
    )

    db.add(new_click)
    db.commit()

    return {"ok": True}

from fastapi import APIRouter, Cookie, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Like

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.get("/journey")
def show_journey_images(
    pagesize: int,
    offset: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    # 한 페이지에 표시할 전체 outfit
    outfits = db.query(Outfit).offset(offset).limit(pagesize).all()
    # 마지막 페이지인지 확인
    is_last = len(outfits) < pagesize

    # 유저가 좋아요 누른 전체 이미지 목록
    # 비회원일때
    if user_id == guest_id:
        likes = (
            db.query(Like)
            .filter(
                Like.user_id == guest_id,
                Like.session_id == session_id,
                Like.is_deleted is False,
            )
            .all()
        )
    # 회원일때
    else:
        likes = (
            db.query(Like)
            .filter(Like.user_id == user_id, Like.is_deleted is False)
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

    # total_cnt = 64400
    # total_page_count = total_cnt // pagesize + (1 if total_cnt % pagesize else 0)

    return {
        "ok": True,
        "outfits_list": outfits_list,
        "pagesize": pagesize,
        "offset": offset,
        "is_last": is_last,
    }


@router.post("/journey/{outfit_id}/click")
def user_click(
    outfit_id: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
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
    db.refresh(new_click)

    return {"ok": True}


@router.post("/journey/{outfit_id}/like")
def user_like(
    outfit_id: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    db_outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    if db_outfit is None:
        raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")

    # 이전에 좋아요 누른적 있는지 확인
    # 비회원
    if user_id == guest_id:
        already_like = db.query(Like).filter(
            Like.user_id == guest_id,
            Like.session_id == session_id,
            Like.outfit_id == outfit_id,
        )
    # 회원
    else:
        already_like = db.query(Like).filter(
            Like.user_id == user_id, Like.outfit_id == outfit_id
        )
    # 누른적 없으면 DB에 추가
    if not already_like:
        new_like = Like(
            session_id=session_id,
            user_id=user_id,
            outfit_id=outfit_id,
            timestamp=datetime.now(timezone("Asia/Seoul")),
            is_deleted=False,
        )
        db.add(new_like)
        db.commit()
        db.refresh(new_like)
    # 누른적 있으면 취소 여부 바꿔줌
    else:
        already_like.is_delete = ~already_like.is_delete
        db.commit()

    return {"ok": True}


@router.get("/collection")
def show_collection_images(
    pagesize: int,
    offset: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    # 비회원일때
    if user_id == guest_id:
        outfit_ids_list = [
            db.query(Like)
            .filter(
                Like.user_id == guest_id,
                Like.session_id == session_id,
                Like.is_deleted is False,
            )
            .offset(offset)
            .limit(pagesize)
            .all()
        ]
    # 회원일때
    else:
        outfit_ids_list = [
            db.query(Like)
            .filter(Like.user_id == user_id, Like.is_deleted is False)
            .offset(offset)
            .limit(pagesize)
            .all()
        ]

    is_last = len(outfit_ids_list) < pagesize

    if not outfit_ids_list:
        raise HTTPException(status_code=500, detail="좋아요한 사진이 없습니다.")

    outfits_list = list()
    for outfit_id in outfit_ids_list:
        outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id)
        outfit_out = OutfitOut(**outfit.__dict__, is_liked=True)
        outfits_list.append(outfit_out)

    return {
        "ok": True,
        "outfits_list": outfits_list,
        "pagesize": pagesize,
        "offset": offset,
        "is_last": is_last,
    }


@router.get("/journey/{outfit_id}")
def show_single_image(
    outfit_id: int,
    user_id: int = Cookie(None),
    session_id: str = Cookie(None),
    db: Session = Depends(get_db),
    guest_id: int = 1,
):
    outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    if outfit is None:
        raise HTTPException(status_code=500, detail="Outfit not found")

    # 좋아요 눌렀는지 체크
    # 비회원
    if user_id == guest_id:
        user_like = db.query(Like).filter(
            Like.user_id == guest_id,
            Like.session_id == session_id,
            Like.outfit_id == outfit_id,
            Like.is_deleted is False,
        )
    # 회원
    else:
        user_like = db.query(Like).filter(
            Like.user_id == user_id,
            Like.outfit_id == outfit_id,
            Like.is_deleted is False,
        )
    # is_liked : user_like 존재하면 True, 아니면 False
    is_liked = user_like is not None
    outfit_out = OutfitOut(**outfit.__dict__, is_liked=is_liked)

    similar_outfits = db.query(Similar).filter(Similar.outfit_id == outfit_id).first()
    if similar_outfits is None:
        raise HTTPException(status_code=500, detail="Similar outfits not found")

    similar_outfits_list = list()
    for similar_outfit_id in similar_outfits:
        similar_outfit = (
            db.query(Outfit).filter(Outfit.outfit_id == similar_outfit_id).first()
        )
        if similar_outfit is None:
            raise HTTPException(
                status_code=500, detail="Id for this similar outfit not found"
            )
        # 좋아요 눌렀는지 체크
        # 비회원
        if user_id == guest_id:
            user_like = db.query(Like).filter(
                Like.user_id == guest_id,
                Like.session_id == session_id,
                Like.outfit_id == similar_outfit_id,
                Like.is_deleted is False,
            )
        # 회원
        else:
            user_like = db.query(Like).filter(
                Like.user_id == user_id,
                Like.outfit_id == similar_outfit_id,
                Like.is_deleted is False,
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

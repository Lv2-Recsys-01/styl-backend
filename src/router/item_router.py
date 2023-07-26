import random
from datetime import datetime
from typing import Annotated

from fastapi import (APIRouter, BackgroundTasks, Cookie, Depends,
                     HTTPException, Path, Query, status)
from pytz import timezone
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..logging import (log_click_image, log_click_share_musinsa,
                       log_view_image, update_last_action_time)
from ..ML.MAB import load_model
from ..models import Click, Like, Outfit, Similar, UserSession
from ..schema import OutfitOut
import numpy as np

router = APIRouter(
    prefix="/api/items",
    tags=["items"],
)

@router.get("/journey")
def show_journey_images(
    background_tasks: BackgroundTasks,
    page_size: Annotated[int, Query()],
    offset: Annotated[int, Query()],
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
) -> dict:
    # 남/여 구분 x
    # outfits = (
    #     db.query(Outfit).order_by(func.random()).offset(offset).limit(page_size).all()
    # )

    # f_outfits = (
    #     db.query(Outfit)
    #     .filter(Outfit.gender == "F")
    #     .order_by(func.random())
    #     .limit(page_size // 2)
    #     .all()
    # )

    # m_outfits = (
    #     db.query(Outfit)
    #     .filter(Outfit.gender == "M")
    #     .order_by(func.random())
    #     .limit(page_size - (page_size // 2))
    #     .all()
    # )

    # outfits = f_outfits + m_outfits

    ### 바꾼 코드 입니다 (상우가) ###
    # load_model 함수는 MAB 모델과 함께 dict들을 불러옵니다
    # MAB 라는 Table이 있어야 합니다!
    model, tag2idx, idx2tag, outfit2idx, idx2outfit = load_model()
    model.alpha = np.array(db.query(MAB).filter(MAB.session_id == session_id).first().alpha)
    model.beta = np.array(db.query(MAB).filter(MAB.session_id == session_id).first().beta)

    # model에서 sample page_size 개 뽑기
    outfits = model.sample(page_size).tolist()

    # beta 분포의 beta 업데이트
    for outfit in outfits:
        model.view(outfit)

    # 이렇게 코드를 짜도 되는지 모르겠지만..? MAB 테이블 업데이트 합니다!
    db.query(MAB).filter(MAB.session_id == session_id).update({"alpha": model.alpha.tolist(), "beta": model.beta.tolist()})

    # idx인 outfit을 outfit_id로 바꾸어 줍니다
    outfits = list(map(idx2outfit.get, outfits))
    random.shuffle(outfits)
    ### 여기까지가 바뀐 코드입니다 ###

    # 마지막 페이지인지 확인
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

    background_tasks.add_task(update_last_action_time,
                              user_id=user_id,
                              session_id=session_id,
                              db=db)

    background_tasks.add_task(log_view_image,
                              user_id=user_id,
                              session_id=session_id,
                              outfits_list=outfits_list,
                              view_type="journey")

    return {
        "ok": True,
        "outfits_list": outfits_list,
        "page_size": page_size,
        "offset": offset,
        "is_last": is_last,
    }


@router.get("/collection")
def show_collection_images(
    background_tasks: BackgroundTasks,
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
            .limit(page_size + 1)
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
            .limit(page_size + 1)
            .all()
        )
    is_last = len(liked_list) <= page_size
    if len(liked_list) == page_size + 1:
        liked_list.pop()

    if len(liked_list) == 0 or not liked_list:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail="좋아요한 사진이 없습니다.",
        )

    outfits_list = list()
    for liked in liked_list[::-1]:
        liked_outfit = (
            db.query(Outfit).filter(Outfit.outfit_id == liked.outfit_id).first()
        )
        outfit_out = OutfitOut(**liked_outfit.__dict__, is_liked=True)
        outfits_list.append(outfit_out)

    background_tasks.add_task(update_last_action_time,
                              user_id=user_id,
                              session_id=session_id,
                              db=db)

    return {
        "ok": True,
        "outfits_list": outfits_list,
        "page_size": page_size,
        "offset": offset,
        "is_last": is_last,
    }


@router.post("/journey/{outfit_id}/like/{like_type}")
# like_type: ['journey', 'detail']
def user_like(
    background_tasks: BackgroundTasks,
    outfit_id: Annotated[int, Path()],
    like_type: Annotated[str, Path()],
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
):
    db_outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    if db_outfit is None:
        raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")

    if like_type not in ['journey', 'detail']:
        like_type = 'unknown'

    ### 바꾼 코드 입니다 (상우가) ###
    model, tag2idx, idx2tag, outfit2idx, idx2outfit = load_model()

    # alpha beta 불러오기
    model.alpha = np.array(db.query(MAB).filter(MAB.session_id == session_id).first().alpha)
    model.beta = np.array(db.query(MAB).filter(MAB.session_id == session_id).first().beta)

    # click 하거나 like 했으므로 update
    model.click_like(outfit2idx[outfit_id])

    # DB에 업데이트!
    db.query(MAB).filter(MAB.session_id == session_id).update({"alpha": model.alpha.tolist(), "beta": model.beta.tolist()})
    ### 여기까지가 바뀐 코드입니다 ###


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
            like_type=like_type,
            as_login=bool(user_id)
        )
        db.add(new_like)
        db.commit()
        background_tasks.add_task(update_last_action_time,
                              user_id=user_id,
                              session_id=session_id,
                              db=db)

        return {"ok": True}
    # 누른적 있으면 업데이트
    else:
        already_like.is_deleted = not bool(already_like.is_deleted)  # type: ignore
        already_like.timestamp = datetime.now(timezone("Asia/Seoul")) # type: ignore
        already_like.like_type = like_type
        db.commit()
        background_tasks.add_task(update_last_action_time,
                              user_id=user_id,
                              session_id=session_id,
                              db=db)

        return {"ok": True}


@router.get("/journey/{outfit_id}")
def show_single_image(
    background_tasks: BackgroundTasks,
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

    background_tasks.add_task(update_last_action_time,
                              user_id=user_id,
                              session_id=session_id,
                              db=db)

    background_tasks.add_task(log_view_image,
                              user_id=user_id,
                              session_id=session_id,
                              outfits_list=similar_outfits_list,
                              view_type="similar")

    return {
        "ok": True,
        "outfit": outfit_out,
        "similar_outfits_list": similar_outfits_list,
    }


@router.post("/journey/{outfit_id}/click/{click_type}")
# click_type: ['journey', 'collection', 'similar']
def user_click(
    background_tasks: BackgroundTasks,
    outfit_id: Annotated[int, Path()],
    click_type: Annotated[str | None, Path()],
    user_id: Annotated[int | None, Cookie()] = None,
    session_id: Annotated[str | None, Cookie()] = None,
    db: Session = Depends(get_db),
):
    db_outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    if db_outfit is None:
        raise HTTPException(status_code=500, detail="해당 이미지는 존재하지 않습니다.")

    if click_type not in ["journey", "collection", "similar"]:
        click_type = "unknown"

    ### 바꾼 코드 입니다 (상우가) ###
    model, tag2idx, idx2tag, outfit2idx, idx2outfit = load_model()

    # alpha beta 불러오기
    model.alpha = np.array(db.query(MAB).filter(MAB.session_id == session_id).first().alpha)
    model.beta = np.array(db.query(MAB).filter(MAB.session_id == session_id).first().beta)

    # click 하거나 like 했으므로 update
    model.click_like(outfit2idx[outfit_id])

    # DB에 업데이트!
    db.query(MAB).filter(MAB.session_id == session_id).update({"alpha": model.alpha.tolist(), "beta": model.beta.tolist()})
    ### 여기까지가 바뀐 코드입니다 ###

    background_tasks.add_task(update_last_action_time,
                              user_id=user_id,
                              session_id=session_id,
                              db=db)

    background_tasks.add_task(log_click_image,
                              user_id=user_id,
                              session_id=session_id,
                              outfit_id=outfit_id,
                              click_type=click_type,
                            )

    return {"ok": True}


@router.post("/journey/{outfit_id}/musinsa-share/{click_type}")
# click_type: ['musinsa', 'share']
def click_share_musinsa(
    outfit_id: Annotated[int, Path()],
    click_type: Annotated[str, Path()],
    background_tasks: BackgroundTasks,
    session_id: Annotated[str | None, Cookie()] = None,
    user_id: Annotated[int | None, Cookie()] = None,
    db: Session = Depends(get_db),
):
    if click_type not in ["share", "musinsa"]:
        click_type = "unknown"

    background_tasks.add_task(update_last_action_time,
                              user_id=user_id,
                              session_id=session_id,
                              db=db)

    background_tasks.add_task(log_click_share_musinsa,
                              session_id = session_id,
                              user_id = user_id,
                              outfit_id = outfit_id,
                              click_type=click_type)

    return {"ok": True}


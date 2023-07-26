from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
from ..models import Click, Like, Outfit, Similar, UserSession, MAB


def get_recommendation(db: Session,
                       likes: list | None,
                       page_size: int,
                       style_type: str='season_2',
                       style_rec_cnt: int=4,
                       sim_rec_cnt: int=4) -> list:
    if style_rec_cnt + sim_rec_cnt > page_size:
        style_rec_cnt = round(page_size * style_rec_cnt / (style_rec_cnt + sim_rec_cnt))
        sim_rec_cnt = page_size - style_rec_cnt
    if style_type not in ['no_season', 'season_1', 'season_2']:
        style_type = 'season_2'
    
    outfits = list()
    style_cand = list() # 카테고리 기반 추천 후보
    sim_cand = list() # 유사 아이템 기반 추천 후보
    if likes:
        for like in likes:
            outfit_id = like.outfit_id
            outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()  # type: ignore
            if outfit:
                style_id = getattr(outfit, f"{style_type}")
                style_cand.append(style_id)
            similar = db.query(Similar).filter(Similar.outfit_id == outfit_id).first()
            if similar:
                sim_cand.extend(similar.similar_outfits) # type: ignore

        k = round(len(likes)/2)
        style_recs = np.random.choice(style_cand, size=min(style_rec_cnt, k)).tolist()
        unique_outfits, counts = np.unique(sim_cand, return_counts=True)
        sim_recs = np.random.choice(unique_outfits, size=min(sim_rec_cnt, k),
                                replace=False, p=counts/counts.sum()).tolist()
        
        for style_id in style_recs:
            outfit = db.query(Outfit).filter(getattr(Outfit, f"{style_type}") == style_id).order_by(func.random()).first()
            if outfit:
                outfits.append(outfit)
        for outfit_id in sim_recs:
            outfit = db.query(Outfit).filter(Outfit.outfit_id==outfit_id).first()
            if outfit:
                outfits.append(outfit)
        # print("outfits:", [o.outfit_id for o in outfits])
        # print("cnt:", len([o.outfit_id for o in outfits]))
    if len(outfits) < page_size:
        k = page_size - len(outfits)
        
        f_outfits = (
            db.query(Outfit)
            .filter(Outfit.gender == "F")
            .order_by(func.random())
            .limit(k // 2)
            .all()
        )
        m_outfits = (
            db.query(Outfit)
            .filter(Outfit.gender == "M")
            .order_by(func.random())
            .limit(k - (k // 2))
            .all()
        )
        outfits += f_outfits + m_outfits
    
    # print("final outfits:", [o.outfit_id for o in outfits])
    # print("cnt:", len([o.outfit_id for o in outfits]))
    np.random.shuffle(outfits)
    print("content based:", [outfit.outfit_id for outfit in outfits])
    return outfits
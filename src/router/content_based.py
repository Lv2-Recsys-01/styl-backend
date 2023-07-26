from sqlalchemy.orm import Session
from sqlalchemy import func
import numpy as np
from ..models import Click, Like, Outfit, Similar, UserSession, MAB


def get_recommendation(db: Session,
                       likes: list | None,
                       total_rec_cnt: int,
                       cat_type: str='cat_gpt',
                       sim_type: str='gpt',
                       cat_rec_cnt: int=4,
                       sim_rec_cnt: int=4) -> list:
    if cat_rec_cnt + sim_rec_cnt > total_rec_cnt:
        cat_rec_cnt = round(total_rec_cnt * cat_rec_cnt / (cat_rec_cnt + sim_rec_cnt))
        sim_rec_cnt = total_rec_cnt - cat_rec_cnt
    if cat_type not in ['cat_gpt', 'cat_base']:
        cat_type = 'cat_gpt'
    if sim_type not in ['gpt', 'kkma']:
        sim_type = 'gpt'
    
    outfits = list()
    cat_cand = list() # 카테고리 기반 추천 후보
    sim_cand = list() # 유사 아이템 기반 추천 후보
    if likes:
        for like in likes:
            outfit_id = like.outfit_id
            outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
            if outfit:
                cat_id = getattr(outfit, f"{cat_type}")
                cat_cand.append(cat_id)
            similar = db.query(Similar).filter(Similar.outfit_id == outfit_id).first()
            if similar:
                similar_list = getattr(similar, f"{sim_type}")
                sim_cand.extend(similar_list)

        k = round(len(likes)/2)
        cat_recs = np.random.choice(cat_cand, size=min(cat_rec_cnt, k)).tolist()
        unique_outfits, counts = np.unique(sim_cand, return_counts=True)
        sim_recs = np.random.choice(unique_outfits, size=min(sim_rec_cnt, k),
                                replace=False, p=counts/counts.sum()).tolist()
        
        for cat_id in cat_recs:
            outfit = db.query(Outfit).filter(getattr(Outfit, f"{cat_type}") == cat_id).order_by(func.random()).first()
            if outfit:
                outfits.append(outfit)
        for outfit_id in sim_recs:
            outfit = db.query(Outfit).filter(Outfit.outfit_id==outfit_id).first()
            if outfit:
                outfits.append(outfit)
        # print("outfits:", [o.outfit_id for o in outfits])
        # print("cnt:", len([o.outfit_id for o in outfits]))
    if len(outfits) < total_rec_cnt:
        k = total_rec_cnt - len(outfits)
        
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
    # return [outfit.outfit_id for outfit in outfits]
    return outfits
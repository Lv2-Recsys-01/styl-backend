import numpy as np
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..models import MAB, Click, Like, Outfit, Similar, UserSession


def get_recommendation(
    db: Session,
    likes: list | None,
    total_rec_cnt: int,
    rec_type: str = "cand",  # 서빙용 추천 목적 or mab 후보 생성 목적
    cat_type: str = "cat_base", # 어떤 카테고리 사용할건지
    sim_type: str = "mixed", # 어떤 유사도 사용할건지
    cat_rec_cnt: int = 4,
    sim_rec_cnt: int = 4,
) -> list:
    if cat_rec_cnt + sim_rec_cnt > total_rec_cnt:
        cat_rec_cnt = round(total_rec_cnt * cat_rec_cnt / (cat_rec_cnt + sim_rec_cnt))
        sim_rec_cnt = total_rec_cnt - cat_rec_cnt
    if rec_type not in ["cand", "rec"]:
        rec_type = "rec"
    if cat_type not in ["cat_gpt", "cat_base"]:
        cat_type = "cat_gpt"
    if sim_type not in ["mixed", "gpt", "kkma"]:
        sim_type = "mixed"

    outfits = list()
    cat_cand = list()  # 카테고리 기반 추천 후보
    sim_cand = list()  # 유사 아이템 기반 추천 후보
    if likes:
        for like in likes:
            outfit_id = like.outfit_id
            outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
            if outfit:
                cat_id = getattr(outfit, f"{cat_type}")
                cat_cand.append(cat_id)
            similar = db.query(Similar).filter(Similar.outfit_id == outfit_id).first()
            if similar:
                if sim_type == 'mixed':
                    similar_list = list(set(similar.kkma + similar.gpt))
                else:
                    similar_list = getattr(similar, f"{sim_type}")
                sim_cand.extend(similar_list)

        if rec_type == "rec":
            k = round(len(likes) / 2)
            replace = False
        else:
            k = len(likes) * 5
            replace = True
        cat_recs = np.random.choice(cat_cand, size=min(cat_rec_cnt, k)).tolist()
        unique_outfits, counts = np.unique(sim_cand, return_counts=True)
        sim_recs = np.random.choice(
            unique_outfits,
            size=min(sim_rec_cnt, k),
            replace=replace,
            p=counts / counts.sum(),
        ).tolist()
        # print("cat_recs", cat_recs)
        # print("sim_recs", sim_recs)
        for cat_id in cat_recs:
            outfit = (
                db.query(Outfit)
                .filter(getattr(Outfit, f"{cat_type}") == cat_id)
                .order_by(func.random())
                .first()
            )
            if outfit:
                outfits.append(outfit)
        for outfit_id in sim_recs:
            outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
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
        # print("random", f_outfits + m_outfits)
        outfits += f_outfits + m_outfits

    # print("final outfits:", [o.outfit_id for o in outfits])
    # print("cnt:", len([o.outfit_id for o in outfits]))
    np.random.shuffle(outfits)
    # print("content based:", [outfit.outfit_id for outfit in outfits])

    return outfits

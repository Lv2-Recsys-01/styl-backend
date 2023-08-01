from typing import Annotated

import numpy as np
from sqlalchemy.orm import Session

from ..models import MAB, Click, Like, Outfit, Similar, UserSession


class MultiArmedBandit(object):
    def __init__(
        self,
        n_unique_tags: int,
    ):
        self.n_arms = n_unique_tags
        self.alpha = np.ones(n_unique_tags)
        self.beta = np.ones(n_unique_tags)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def sample(self,
               cand_outfit_list: list,
               cand_tag_list: list[np.array],
               n_samples: int):
        tag_score = np.array([])
        for i in range(self.n_arms):
            tag_score = np.append(tag_score, np.random.beta(max(1, self.alpha[i]),
                                                            max(1, self.beta[i])))

        outfit_score = []
        for tags in cand_tag_list:
            outfit_score.append(np.mean(tag_score[tags]))

        probs = self.softmax(outfit_score)
        samples = np.random.choice(
            cand_outfit_list, n_samples, replace=False, p=probs
        ).tolist()

        return samples


def get_mab_model(
    user_id: int | None, session_id: str | None, db: Session
) -> MultiArmedBandit:
    n_unique_tags = 200
    mab_model = MultiArmedBandit(n_unique_tags)

    # db에 있으면 불러오고
    if user_id is None:
        mab_params = (
            db.query(MAB)
            .filter(MAB.user_id.is_(None), MAB.session_id == session_id)
            .first()
        )
    else:
        mab_params = (
            db.query(MAB)
            .filter(MAB.session_id.is_(None), MAB.user_id == user_id)
            .first()
        )
    # 없으면 만들고 db에 추가
    if mab_params is None:
        if user_id is not None:
            session_id = None
        mab_params = MAB(
            session_id=session_id,
            user_id=user_id,
            alpha=[1] * n_unique_tags,
            beta=[1] * n_unique_tags,
        )

        db.add(mab_params)
        db.commit()

    mab_model.alpha = np.array(mab_params.alpha)
    mab_model.beta = np.array(mab_params.beta)

    return mab_model


async def update_ab(
    user_id: int | None,
    session_id: str,
    db: Session,
    outfit_id_list: list[int],
    reward_list: list[int],
    interaction_type: str,
):
    if interaction_type not in ["view_journey",
                                "view_similar",
                                "click_journey",
                                "click_similar",
                                "like",
                                "like_cancel"]:
        return
    if user_id is None:
        mab_params = (
            db.query(MAB)
            .filter(MAB.session_id == session_id, MAB.user_id.is_(None))
            .first()
        )
    else:
        mab_params = (
            db.query(MAB)
            .filter(MAB.session_id.is_(None), MAB.user_id == user_id)
            .first()
        )

    alpha = np.array(mab_params.alpha)
    beta = np.array(mab_params.beta) 
    # interaction 종류에 따라 알파, 배타 업데이트
    for outfit_id, reward in zip(outfit_id_list, reward_list):
        outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
        tags = np.array(list(map(int, outfit.tags_filtered)))
        # tags = np.array(outfit.tags_filtered)
        if interaction_type == "view_journey":
            # alpha[tags] += reward
            beta[tags] += 1 - reward
        elif interaction_type == "view_similar":
            # alpha[tags] += reward
            beta[tags] += 0.5 - reward
        elif interaction_type == "click_journey":
            alpha[tags] += reward * 2
            beta[tags] += -reward
        elif interaction_type == "click_similar":
            alpha[tags] += reward * 2
            beta[tags] += -reward * 0.5
        elif interaction_type == "like":
            alpha[tags] += reward * 5
            beta[tags] += -reward
        elif interaction_type == "like_cancel":
            alpha[tags] += -reward * 5
            beta[tags] += reward

    mab_params.alpha = alpha.tolist()
    mab_params.beta = beta.tolist()
    print("interaction:", interaction_type)
    print("alpha updated:", sum(mab_params.alpha))
    print("beta updated:", sum(mab_params.beta))

    db.commit()


def get_mab_recommendation(
    mab_model: MultiArmedBandit,
    user_id: int | None,
    session_id: str,
    db: Session,
    cand_outfit_list: list,
    n_samples: int = 10,
):
    if user_id is None:
        mab_params = (
            db.query(MAB)
            .filter(MAB.session_id == session_id, MAB.user_id.is_(None))
            .first()
        )
    else:
        mab_params = (
            db.query(MAB)
            .filter(MAB.session_id.is_(None), MAB.user_id == user_id)
            .first()
        )
    mab_model.alpha = mab_params.alpha
    mab_model.beta = mab_params.beta

    # 후보군 각 아이템의 태그 저장
    cand_tag_list = list()
    for outfit_id in cand_outfit_list:
        cand_tag = (
            db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first().tags_filtered
        )
        cand_tag = list(map(int, cand_tag))
        cand_tag_list.append(np.array(cand_tag))

    mab_recs = mab_model.sample(cand_outfit_list, cand_tag_list, n_samples)

    # outfits = list()
    # for outfit_id in mab_recs:
    #     outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
    #     outfits.append(outfit)
        
    outfits = db.query(Outfit).filter(Outfit.outfit_id.in_(mab_recs)).all()

    np.random.shuffle(outfits)
    return outfits

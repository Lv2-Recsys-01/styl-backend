import numpy as np
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import (APIRouter, BackgroundTasks, Cookie, Depends, HTTPException, Path, Query,
                     status)
from ..models import Click, Like, Outfit, Similar, UserSession, MAB


class MultiArmedBandit(object):
    def __init__(self, 
                 n_unique_tags: int,
                #  outfit_id_list: np.ndarray, 
                #  outfit_tag_list: list[np.ndarray],
                 ):
        self.n_arms = n_unique_tags
        self.alpha = np.ones(n_unique_tags)
        self.beta = np.ones(n_unique_tags)
        # self.outfit_id_list = outfit_id_list
        # self.outfit_tag_list = outfit_tag_list
        
    def softmax(self, x):
        e_x = np.exp(x - np.max(x))  # subtract max for numerical stability
        return e_x / e_x.sum(axis=0)
        
    def sample(self, cand_id_list: list, cand_tag_list: list, n_samples: int):
        tag_score = []
        for i in range(self.n_arms):
            tag_score.append(np.random.beta(self.alpha[i], self.beta[i]))
        tag_score = np.array(tag_score)
        
        outfit_score = []
        for tags in cand_tag_list:
            outfit_score.append(np.mean(tag_score[tags]))
            
        # probs = outfit_score / np.sum(outfit_score)
        probs = self.softmax(outfit_score)
        samples = np.random.choice(cand_id_list, n_samples, replace=False, p=probs).tolist()
        
        return samples
    
    
def get_mab_model(user_id: int | None,
                  session_id: str,
                  db: Session):
    # n_unique_tags = 1879 # 이거 하드코딩 안하고 가능??
    n_unique_tags = 200
    # all_outfit = db.query(Outfit).all()
    # outfit_id_list = np.array([outfit.outfit_id for outfit in all_outfit])
    # outfit_tag_list = [np.array(outfit.tags) for outfit in all_outfit]
    # outfit_tag_list = [np.array(outfit.tags_filtered) for outfit in all_outfit]
        
    mab_model = MultiArmedBandit(n_unique_tags,
                                #  outfit_id_list, outfit_tag_list,
                                 )
    
    # db에 있으면 불러오고
    if user_id is None:
        mab = db.query(MAB).filter(MAB.user_id.is_(None),
                                         MAB.session_id == session_id).first()
    else:
        mab = db.query(MAB).filter(MAB.session_id.is_(None),
                                         MAB.user_id == user_id).first()
    # 없으면 만들고 db에 추가
    if mab is None:
        if user_id is not None:
            session_id = None
        mab = MAB(
                session_id=session_id,
                user_id=user_id,
                alpha = [1] * n_unique_tags,
                beta = [1] * n_unique_tags           
            )
    
        db.add(mab)
        db.commit()
    
    mab_model.alpha = np.array(mab.alpha)
    mab_model.beta = np.array(mab.beta)
    
    return mab_model


async def update_ab(user_id: int | None,
                    session_id: str,
                    db: Session,
                    outfit_id_list: list[int],
                    reward_list: list[int],
                    interaction_type: str):
    if interaction_type not in ['view', 'click_like', 'like_cancel']:
        interaction_type = 'view'
    if user_id is None:
        mab = db.query(MAB).filter(MAB.session_id == session_id,
                                      MAB.user_id.is_(None)).first()
    else:
        mab = db.query(MAB).filter(MAB.session_id.is_(None),
                                      MAB.user_id == user_id).first()
    alpha = np.array(mab.alpha)
    beta = np.array(mab.beta)
    for outfit_id, reward in zip(outfit_id_list, reward_list):
        outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
        tags = np.array(outfit.tags_filtered)
        if interaction_type == 'view':
            alpha[tags] += reward
            beta[tags] += (1 - reward)
        elif interaction_type == 'click_like':
            alpha[tags] += reward * 5
            beta[tags] += -reward
        elif interaction_type == 'like_cancel':
            alpha['tags'] += -reward * 5
            beta['tags'] += reward
            
    mab.alpha = alpha.tolist()
    mab.beta = alpha.tolist()
    
    print("alpha, beta updated")
    print("alpha:", sum(alpha))
    print("beta:", sum(beta))
    db.commit()


def get_mab_recommendation(mab_model: MultiArmedBandit,
                           user_id: int | None,
                           session_id: str,
                           db: Session,
                           cand_id_list: list,
                           n_samples: int=10):
    if user_id is None:
        mab = db.query(MAB).filter(MAB.session_id == session_id,
                                      MAB.user_id.is_(None)).first()
    else:
        mab = db.query(MAB).filter(MAB.session_id.is_(None),
                                      MAB.user_id == user_id).first()
    mab_model.alpha = mab.alpha
    mab_model.beta = mab.beta

    cand_tag_list = list()
    for outfit_id in cand_id_list:
        cand_tag = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first().tags_filtered
        cand_tag_list.append(np.array(cand_tag))
    
    mab_recs = mab_model.sample(cand_id_list, cand_tag_list, n_samples)
    
    outfits = list()
    for outfit_id in mab_recs:
        outfit = db.query(Outfit).filter(Outfit.outfit_id == outfit_id).first()
        outfits.append(outfit)
    
    np.random.shuffle(outfits)
    # print("mab:", [outfit.outfit_id for outfit in outfits])
    return outfits
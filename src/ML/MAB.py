import ast
import pickle

import numpy as np
import pandas as pd


class MAB(object):
    def __init__(self, num_arms: int, outfits: np.array, tags: np.array, weight: int):
        self.alpha = np.ones(num_arms)
        self.beta = np.ones(num_arms)
        self.outfits = outfits
        self.tags = tags
        self.weight = weight

    # view 했을 시 beta에 weight (1) 만큼 더해주는 코드입니다.
    def view(self, arm):
        for tag in self.tags[arm]:
            self.beta[tag] += self.weight


    # click 혹은 like 했을 시 alpha에 weight 만큼 더해주고, 아까 beta에 더한 값을 빼주는 코드입니다.
    def click_like(self, arm):
        for tag in self.tags[arm]:
            self.alpha[tag] += self.weight
            if (self.beta[tag] - self.weight) > 0:
                self.beta[tag] -= self.weight

    # num_sample 만큼 sampling 해주는 코드입니다.
    def sample(self, num_sample):
        rvs = []
        for i in range(len(self.alpha)):
            rvs.append(np.random.beta(self.alpha[i], self.beta[i]))
        rvs = np.array(rvs)

        probs = []
        for tags in self.tags:
            probs.append(np.mean(rvs[tags]))

        probs = probs / np.sum(probs)
        samples = np.random.choice(self.outfits, num_sample, p=probs)

        return samples

def load_model():
    with open('tag2idx.pickle', 'rb') as f:
        tag2idx = pickle.load(f)
    with open('./idx2tag.pickle', 'rb') as f:
        idx2tag = pickle.load(f)
    with open('./outfit2idx.pickle', 'rb') as f:
        outfit2idx = pickle.load(f)
    with open('./idx2outfit.pickle', 'rb') as f:
        idx2outfit = pickle.load(f)

    outfit4mab = pd.read_csv('./outfit4mab.csv')
    outfit4mab['outfit_id'] = outfit4mab['outfit_id'].map(outfit2idx)
    outfit4mab['gpttag'] = outfit4mab['gpttag'].apply(lambda x: ast.literal_eval(x))

    model = MAB(len(tag2idx), outfit4mab['outfit_id'].values, outfit4mab['gpttag'].values, 10, 1)

    return model, tag2idx, idx2tag, outfit2idx, idx2outfit


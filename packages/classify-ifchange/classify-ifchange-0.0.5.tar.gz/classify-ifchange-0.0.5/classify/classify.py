from nlutools import NLU
from collections import defaultdict
import numpy as np
from scipy.spatial.distance import cosine
from sklearn.metrics import pairwise_distances


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return v / norm

class Classifier:
    def __init__(self, corpus_path, env='dev', dim=512):
        self.nlu = NLU(env=env)
        self.dim = dim
        self.class_dict = defaultdict(list)
        self.corpus = corpus_path
        self.center_dict = {}
        self._build_centers()

    def _build_centers(self):
        with open(self.corpus,'r',encoding='utf-8') as f:
            lines = f.readlines()
            lines = [x.strip().split('\t') for x in lines]
            for line in lines:
                self.class_dict[line[1]].append(line[0])
            for k, v in self.class_dict.items():
                embs = np.asarray(self._get_embs(v))
                center = np.mean(embs, axis=0).squeeze()
                self.center_dict[k] = center
            tps = list(self.center_dict.items())
            self.centers = [x[1] for x in tps]
            self.classes = [x[0] for x in tps]

    def infer_by_input(self):
        while True:
            sent = input("enter a sentence: ")
            res, pclass = self.infer(sent)
            print(res)
            print("predicted class: {}".format(pclass))

    def infer_multiround(self):
        self.emb = np.zeros(self.dim,)
        while True:
            sent = input("enter a sentence: ")
            self.emb += self._get_embs(sent)[0]
            self.emb = normalize(self.emb)
            res, pclass = self.infer(sent, emb=self.emb)
            print("给你推荐这门课: {}".format(pclass))


    def infer(self, sent, emb=None):
        if emb is None:
            emb = self._get_embs(sent)
        res, pclass = self._pred_class(emb)
        return res, pclass

    def infer_sents(self, sents):
        embs = self._get_embs(sents)
        dists = np.asarray(pairwise_distances(embs, self.centers, metric='cosine'))
        preds = np.argmin(dists, axis=-1).squeeze()
        preds = [self.classes[x] for x in preds]
        results = [list(zip(self.classes, dist)) for dist in dists]
        print(preds)
        print(results)
        return results, preds


    def _get_embs(self, sent):
        return self.nlu.bert_encode(sent)['vec']

    def _pred_class(self, emb):
        dists = [cosine(emb, center) for center in self.centers]
        maxind = np.argmin(dists)
        results = list(zip(self.classes, dists))
        return results, self.classes[maxind]

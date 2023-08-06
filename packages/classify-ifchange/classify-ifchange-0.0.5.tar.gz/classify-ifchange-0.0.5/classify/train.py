import torch
from sklearn.model_selection import train_test_split
from torch.optim import Adam
from nlutools import NLU
from classify.network import SimpleClassifier
import numpy as np
from classify.classify import normalize
from collections import Counter
import traceback
import json

class MLPTrainer:
    def __init__(self, mode, epoch=5, batch_size=64, model_path='model/model.h5', cuda=1, dropout=0.2, reverse=False):
        self.nlu = NLU(mode)
        self.device = torch.device("cuda:{}".format(cuda) if torch.cuda.is_available() else 'cpu')
        self.epoch = epoch
        self.batch_size = batch_size
        self.best = 0.
        self.model_path = model_path
        self.dropout = dropout
        self.reverse = reverse
    
    def load_model(self, model_path, classdict_path):
        with open(classdict_path, 'r', encoding='utf-8') as f:
            self.class_dict = json.load(f)
        self.model = torch.load(model_path)

    def infer_by_input(self):
        self.model.eval()
        print(self.class_dict)
        while True:
            sent = input("pls enter a sentence: ")
            emb = self.nlu.bert_encode([sent])['vec']
            emb = torch.FloatTensor(emb).to(self.device)
            res = self.model(emb).tolist()
            res = np.argmax(res, axis=-1).squeeze()
            res = int(res)
            res = self.class_dict[str(res)]
            print(res)

    def train_on_corpus(self, train_path, test_path=None, evaluate=False):
        X, Y = self._load_corpus(train_path, self.reverse)
        test_size = 0.2
        if test_path:
            testX, testY = self._load_corpus(test_path,self.reverse)
            X, Y = X + testX, Y + testY
            print(len(X), len(Y))
            test_size = len(testY)/len(Y)*1.0
        Y = self._process_labels(Y)
        
        trainX, testX, trainY, testY = train_test_split(X, Y, stratify=Y, test_size=test_size, shuffle=True, random_state=123)
        self.model = SimpleClassifier(len(self.labels), dropout=self.dropout)
        self.model.to(self.device)
        self.optimizer = Adam(lr=1e-3, params=self.model.parameters())
        total = len(trainY)
        nstep = total//self.batch_size
        for ep in range(self.epoch):
            print("EPOCH: {}/{}".format(ep, self.epoch))
            for i in range(nstep):

                begin = i*self.batch_size
                end = (i+1)*self.batch_size
                batchX = trainX[begin:end]
                batchY = trainY[begin:end]
                try:
                    loss =self.train_on_batch(batchX, batchY)
                except Exception as e:
                    print(e)
                    loss = 0
                    traceback.print_exc()
                    pass
                if i % 10 == 0:
                    print(loss)
            if evaluate:
                acc = self.evaluate(testX, testY)
                if acc>=self.best:
                    self.best = acc
                    self.save_model()

    def save_model(self):
        torch.save(self.model, self.model_path)

    def evaluate(self, testX, testY):
        self.model.eval()
        total = len(testY)
        nstep = total // self.batch_size
        acc = 0.
        for i in range(nstep):
            #if i % 30==0:
            #    print("  STEP: {}/{}".format(i, nstep))
            begin = self.batch_size*i
            end = (i +1)* self.batch_size
            batchX = testX[begin:end]
            batchY = testY[begin:end]
            preds = self.predict_batch(batchX)
            preds = preds.squeeze().tolist()
            preds = np.argmax(preds, axis=-1)
            res = [1 if x==y else 0 for x,y in zip(batchY, preds)]
            acc += sum(res)/len(res)*1.0
        print("  ACC: ", acc/nstep*1.0)
        return acc

    def predict_batch(self, batchX):
        try:
            batchX = self.nlu.bert_encode(batchX)['vec']
        except:
            print(111)
            print(batchX)
        batchX = torch.FloatTensor(batchX).to(self.device)
        preds = self.model(batchX)
        return preds

    def _process_labels(self, Y):
        self.labels = list(set(Y))
        self.class_dict = {x:y for x,y in enumerate(self.labels)}
        with open('model/class.dict', 'w', encoding='utf-8') as f:
            json.dump(self.class_dict, f)
        self.inv_class_dict = {y:x for x,y in self.class_dict.items()}
        Y = [self.inv_class_dict[x] for x in Y]
        class_weight = Counter(Y)
        self.class_weight = []
        for i in range(len(class_weight)):
            self.class_weight.append(class_weight[i])
        self.class_weight = np.asarray(self.class_weight)/sum(self.class_weight)
        self.class_weight = torch.FloatTensor(self.class_weight).to(self.device)
        print(self.class_weight)
        return Y


    def _load_corpus(self, corpus_path, reverse=False):
        with open(corpus_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines = [x.strip().split('\t') for x in lines]
            lines = [x for x in lines if len(x)==2]
        if not reverse:
            X = [x[0] for x in lines]
            Y = [x[1] for x in lines]
        else:
            X = [x[1] for x in lines]
            Y = [x[0] for x in lines]
        return X, Y


    def train_on_batch(self, batchX, batchY):
        self.model.train()
        batchX = self.nlu.bert_encode(batchX)['vec']
        batchX = torch.FloatTensor(batchX).to(self.device)
        batchY = torch.LongTensor(batchY).to(self.device)
        preds = self.model(batchX)
        loss = self._get_loss(preds, batchY)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def _get_loss(self, preds, targets):
        return torch.nn.CrossEntropyLoss()(preds, targets)

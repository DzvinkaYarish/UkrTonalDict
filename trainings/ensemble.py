from sklearn.cross_validation import train_test_split
import numpy as np
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, classification_report
from nltk.tokenize import TweetTokenizer
import pymorphy2







f = open("/home/dzvinka/PycharmProjects/UkrTonalDict/models/lr.pickle", "rb")
lr = pickle.load(f)
f.close()

f = open("/home/dzvinka/PycharmProjects/UkrTonalDict/models/svm.pickle", "rb")
svc = pickle.load(f)
f.close()

f = open("/home/dzvinka/PycharmProjects/UkrTonalDict/models/random_forest.pickle", "rb")
rf = pickle.load(f)
f.close()


train  = pd.read_csv("/home/dzvinka/PycharmProjects/UkrTonalDict/tips/rewiews_from_ucu_sentiment_lemmatized.csv", sep="|")



data_train, data_test, labels_train, labels_test = \
    train_test_split(train['opinion_text'], train['opinion_rating'],
                     test_size=0.1, random_state=42, stratify=train['opinion_rating'])\



y_pred = lr.predict(data_test)

y_pred_rf = rf.predict(data_test)

print("Logistic regression")
print(f1_score(labels_test, y_pred))
print(classification_report(labels_test, y_pred))
print()

print("RF")
print(f1_score(labels_test, y_pred_rf))
print(classification_report(labels_test, y_pred_rf))
print()

lr_pred = lr.predict_proba(data_test)[:,1]
rf_pred = rf.predict_proba(data_test)[:, 1]
scores = []

for i in np.linspace(0, 1, 10):

    res = i * lr_pred + (1 - i) * rf_pred
    #print(res)
    res = np.array(res >= 0.4, int)

    scr = f1_score(labels_test, res)
    print(i, res, scr)
    # for i in range(len(labels_train)):
    #     if labels_train[i] != res[i]:
    #         print(data_train.iloc[i, 0])
    scores.append((scr,i))



print(max(scores))





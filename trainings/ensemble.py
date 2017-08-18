from sklearn.cross_validation import train_test_split
import numpy as np
import pickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, classification_report
from nltk.tokenize import TweetTokenizer
import pymorphy2



def process_tips(tip):
    words = [word.lower() for word in twtk.tokenize(tip) if word.isalpha()]
    processed_tip = ""
    for i in range(0, len(words)):
        processed_tip +=  morph.parse(words[i])[0].normal_form
        processed_tip += " "

    return processed_tip



twtk = TweetTokenizer()

morph = pymorphy2.MorphAnalyzer(lang='uk')



f = open("/home/dzvinka/PycharmProjects/UkrTonalDict/models/logistic_regr.pickle", "rb")
lr = pickle.load(f)
f.close()

f = open("/home/dzvinka/PycharmProjects/UkrTonalDict/models/svm.pickle", "rb")
svc = pickle.load(f)
f.close()

train  = pd.read_csv("/home/dzvinka/PycharmProjects/UkrTonalDict/tips/rewiews_from_ucu_sentiment_lemmatized.csv", sep="|")

vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=8000)

data_train, data_test, labels_train, labels_test = \
    train_test_split(train['opinion_text'], train['opinion_rating'],
                     test_size=0.1, random_state=42, stratify=train['opinion_rating'])\


x_train = vectorizer.fit_transform(data_train)
x_test = vectorizer.transform(data_test)

y_pred = lr.predict(x_test)

y_pred_svm = svc.predict(x_test)

print("Logistic regression")
print(f1_score(labels_test, y_pred))
print(classification_report(labels_test, y_pred))
print()

print("SVM")
print(f1_score(labels_test, y_pred_svm))
print(classification_report(labels_test, y_pred_svm))
print()

lr_pred = lr.predict_proba(x_test)[:,1]
svc_pred = svc.predict_proba(x_test)[:, 1]
scores = []

for i in np.linspace(0, 1, 10):

    res = i * lr_pred + (1 - i) * svc_pred
    #print(res)
    res = np.array(res >= 0.5, int)

    scr = f1_score(labels_test, res)
    print(i, res, scr)
    # for i in range(len(labels_train)):
    #     if labels_train[i] != res[i]:
    #         print(data_train.iloc[i, 0])
    scores.append((scr,i))



print(max(scores))





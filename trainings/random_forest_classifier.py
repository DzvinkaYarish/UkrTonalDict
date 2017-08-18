from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, classification_report

import pandas as pd

vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=8000)

train  = pd.read_csv("/home/dzvinka/PycharmProjects/UkrTonalDict/tips/rewiews_from_ucu_sentiment_lemmatized.csv", sep="|")

data_train, data_test, labels_train, labels_test = \
    train_test_split(train['opinion_text'], train['opinion_rating'],
                     test_size=0.1, random_state=42, stratify=train['opinion_rating'])
print(data_train.head)

x_train = vectorizer.fit_transform(data_train.values.astype('U'))
x_test = vectorizer.transform(data_test.values.astype('U'))

clf = RandomForestClassifier(n_jobs=4, n_estimators=20)
clf.fit(x_train, labels_train)

y_predict = clf.predict(x_test)

print(f1_score(labels_test, y_predict))
print(classification_report(labels_test, y_predict))

f = open('/home/dzvinka/PycharmProjects/UkrTonalDict/models/random_forest.pickle', 'wb')
pickle.dump(clf, f)
f.close()



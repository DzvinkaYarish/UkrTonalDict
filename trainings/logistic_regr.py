from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer

import pandas as pd

train  = pd.read_csv("/home/dzvinka/PycharmProjects/UkrTonalDict/tips/rewiews_from_ucu_sentiment.csv", sep="|")

vectorizer = TfidfVectorizer(min_df=1)

count_vectorizer = CountVectorizer(max_features=8000)

X = count_vectorizer.fit_transform(train["opinion_text"])
#X = vectorizer.fit_transform(train["opinion_text"])
#X = X.A
#print(X.A)

#data_train= train["opinion_text"][100:]
#data_test  = train["opinion_text"][:100]

data_train = X[100:]
data_test = X[:100]
labels_train = train["opinion_rating"][100:]
labels_test  = train["opinion_rating"][:100]

lr = LogisticRegression(C=1000.0).fit(data_train, labels_train)

print("Training set accuracy: {:.2f}".format(lr.score(data_train, labels_train)))

print("Test set accuracy: {:.2f}".format(lr.score(data_test, labels_test)))

print(lr.predict(X[0]))


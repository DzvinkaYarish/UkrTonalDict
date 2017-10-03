from sklearn.cross_validation import train_test_split
from sklearn.pipeline import Pipeline
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, classification_report
from nltk.tokenize import TweetTokenizer
import pandas as pd

twtk = TweetTokenizer()

# Data loading
train = pd.read_csv("../tips/ukrainian_lemmatized.csv", sep="|")
train = train[train['opinion_text'].notnull()]

# Spling data into train and test  sets
data_train, data_test, labels_train, labels_test = \
    train_test_split(train['opinion_text'], train['opinion_rating'],
                     test_size=0.1, random_state=42, stratify=train['opinion_rating'])\

# include tokenizer=twtk.tokenize in Tfidf in case you need to change tokenization
mdl_lr = Pipeline([('tfidf', TfidfVectorizer(ngram_range=(1, 3), max_features=10000)), ('lr', LogisticRegression(C=10.0, n_jobs=-1))])
mdl_lr.fit(data_train, labels_train)

y_pred_lr = mdl_lr.predict(data_test)

print("Logistic regression")
print(f1_score(labels_test, y_pred_lr))
print(classification_report(labels_test, y_pred_lr))

# Model saving
print("Saving LR model to file")
f = open('../models/lr.pickle', 'wb')
pickle.dump(mdl_lr, f)
f.close()

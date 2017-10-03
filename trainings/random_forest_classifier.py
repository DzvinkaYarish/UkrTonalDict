from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV


import pandas as pd



train  = pd.read_csv("/home/dzvinka/PycharmProjects/UkrTonalDict/tips/rewiews_from_ucu_sentiment_lemmatized.csv", sep="|")
train = train[train['opinion_text'].notnull()]

data_train, data_test, labels_train, labels_test = \
    train_test_split(train['opinion_text'], train['opinion_rating'],
                     test_size=0.1, random_state=42, stratify=train['opinion_rating'])
#print(data_train.head)


pipeline = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 3), max_features=8000)), ("rf", RandomForestClassifier(n_jobs=-1, n_estimators=25))])

parameters_grid = {"rf__min_samples_leaf": [5, 25],
                   "rf__min_samples_split": [20]}
                   #"rf__n_estimators":  [10, 15, 20, 25]}

clf_grid = GridSearchCV(estimator=pipeline, param_grid=parameters_grid)


clf_grid.fit(data_train, labels_train)

print(clf_grid.best_params_)

y_predict = clf_grid.predict(data_test)

print(f1_score(labels_test, y_predict))
print(classification_report(labels_test, y_predict))

f = open('/home/dzvinka/PycharmProjects/UkrTonalDict/models/random_forest.pickle', 'wb')
pickle.dump(clf_grid, f)
f.close()



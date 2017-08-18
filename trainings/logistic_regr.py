from sklearn.cross_validation import train_test_split
from sklearn.svm import SVC
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import f1_score, classification_report
from nltk.tokenize import TweetTokenizer
import pymorphy2

import pandas as pd

twtk = TweetTokenizer()

morph = pymorphy2.MorphAnalyzer(lang='uk')


def process_tips(tip):
    words = [word.lower() for word in twtk.tokenize(tip) if word.isalpha()]
    processed_tip = ""
    for i in range(0, len(words)):
        processed_tip +=  morph.parse(words[i])[0].normal_form
        processed_tip += " "

    return processed_tip




#load data
train  = pd.read_csv("/home/dzvinka/PycharmProjects/UkrTonalDict/tips/rewiews_from_ucu_sentiment_lemmatized.csv", sep="|")

#clean and lemmatize reviews
# arr = train.as_matrix(columns=["opinion_text"])
#
# for i in range(train.shape[0]):
#
#     train.set_value(i, "opinion_text",  process_tips(arr[i][0]))
#
# train.to_csv("/home/dzvinka/PycharmProjects/UkrTonalDict/tips/rewiews_from_ucu_sentiment_lemmatized", sep="|", index=False)
# print("written")




#split data into test and training sets
data_train, data_test, labels_train, labels_test = \
    train_test_split(train['opinion_text'], train['opinion_rating'],
                     test_size=0.1, random_state=42, stratify=train['opinion_rating'])\


#use tf-idf representation of documents
vectorizer = TfidfVectorizer(ngram_range=(1, 3), max_features=8000)
x_train = vectorizer.fit_transform(data_train)
x_test = vectorizer.transform(data_test)


#train models
lr = LogisticRegression(C=10.0).fit(x_train, labels_train)

mysvc = SVC(C=10.0, kernel="linear", probability=True).fit(x_train, labels_train)


# print("Training set accuracy: {:.2f}".format(mysvc.score(x_train, labels_train)))
#
# print("Test set accuracy: {:.2f}".format(mysvc.score(x_test, labels_test)))


#test models
y_pred = lr.predict(x_test)

y_pred_svm = mysvc.predict(x_test)

print("Logistic regression")
print(f1_score(labels_test, y_pred))
print(classification_report(labels_test, y_pred))
print()

print("SVM")
print(f1_score(labels_test, y_pred_svm))
print(classification_report(labels_test, y_pred_svm))
print()


#save models
print("save lr model to file")
f = open('/home/dzvinka/PycharmProjects/UkrTonalDict/models/logistic_regr.pickle', 'wb')
pickle.dump(lr, f)
f.close()

print("save svm model to file")
f = open('/home/dzvinka/PycharmProjects/UkrTonalDict/models/svm.pickle', 'wb')
pickle.dump(mysvc, f)
f.close()



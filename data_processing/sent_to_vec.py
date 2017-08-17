import sys
import os

import numpy as np
from gensim.models import KeyedVectors
from sklearn.neighbors import KNeighborsClassifier


def read_sentiments(filename):
    f = open(filename)
    data = [s.strip().split(':') for s in f.readlines()]
    sentiments = {}

    for dt in data:
        val = int(dt[1])
        if val in sentiments:
            sentiments[val].append(dt[0])
        else:
            sentiments[val] = [dt[0]]

    return sentiments

def save_vectors(sentiments, out_path):
    print('loading word2vec started')
    word2vecModel = KeyedVectors.load_word2vec_format('/home/dzvinka/PycharmProjects/UkrTonalDict/models/fiction.lowercased.tokenized.word2vec.300d', binary=False)
    print('loading word2vec finished')

    word2vecModel.init_sims(replace=True)

    if not os.path.exists(out_path):
        os.mkdir(out_path)

    for sentiment in sentiments:
        data = None
        for word in sentiments[sentiment]:
            if word not in word2vecModel:
                print("word '%s' not in vocabulary" % word)
                continue
            if data is None:
                data = np.array([word2vecModel[word]])
            else:
                data = np.vstack((data, word2vecModel[word]))


        if out_path[-1] != '/':
            out_path += '/'

        out_file = out_path + 'words_%d.npy' % sentiment

        np.save(out_file, data)

def load_vectors(path):
    X = None
    y = None

    for file in os.listdir(path):
        if path[-1] != '/':
            path += '/'
        filename = path + file

        data = np.load(filename)

        if X is None:
            X = data
        else:
            X = np.concatenate((X, data))

        cl = int(file.split('_')[1][:-4])

        if y is None:
            y = np.ones((len(data))) * cl
        else:
            y = np.hstack((y, np.ones((len(data))) * cl))

    return X, y


#save_vectors(read_sentiments("/home/dzvinka/PycharmProjects/UkrTonalDict/dictionaries/my_sentiment_dict.txt"), 'vectors/')
X, y = load_vectors('vectors/')

X_train = X[100:]
y_train = y[100:]
X_test = X[:100]
y_test = y[:100]


knn = KNeighborsClassifier(n_neighbors = 9)
knn.fit(X_train, y_train)
print('Accuracy of K-NN classifier on training set: {:.2f}'
     .format(knn.score(X_train, y_train)))
print('Accuracy of K-NN classifier on test set: {:.2f}'
     .format(knn.score(X_test, y_test)))
import numpy as np

from gensim.models import word2vec
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, MaxPooling1D, Convolution1D


from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer

from sklearn.cross_validation import train_test_split

#=================================================Parameters section====================================================
#data preprocessing params
sequence_length = 50
max_words=5000

#word2vec params
num_features = 400    # Word vector dimensionality
min_word_count = 10   # Minimum word count
num_workers = -1       # Number of threads to run in parallel
context = 10          # Context window size
downsampling = 1e-3   # Downsample setting for frequent words

#Model Hyperparams
embedding_dim = num_features
filter_size = 3
num_filters = 10
dropout_prob = (0.5, 0.8)
hidden_dims = 50

# Training parameters
batch_size = 64
num_epochs = 10



X = []
Y = []


with open('../tips/rewiews_from_ucu_sentiment_lemmatized.csv') as file:
    file.readline()
    for line in file.readlines():
        X.append(line.split('|')[1])
        Y.append(int(line.split('|')[0]))


tok = Tokenizer(num_words=max_words)
tok.fit_on_texts(X)
sequences = tok.texts_to_sequences(X)
padded_seq = sequence.pad_sequences(sequences, maxlen=sequence_length)

vocabulary = dict((v,k) for k, v in tok.word_index.items())



#Generate word2vec embeddings
print('Generating word embeddings...')
model = word2vec.Word2Vec(X, workers=num_workers,
            size=num_features, min_count = min_word_count)


model.init_sims(replace=True)

vectors = model.wv
#print(vocabulary)
data = []
for seq in padded_seq:
    tmp = []
    for index in seq:
        try:
            tmp.append(vectors[vocabulary[index]])
        except KeyError:
            tmp.append([0]*embedding_dim)
    data.append(tmp)


# # It can be helpful to create a meaningful model name and
# # save the model for later use. You can load it later using Word2Vec.load()
# model_name = '300features_20minwords_10context'
# model.save(model_name)
# print('Model saved')

x_train, x_test, y_train, y_test = train_test_split(data, Y, test_size=0.2, stratify=Y)

#Build model
model = Sequential()
model.add(Convolution1D(filters=num_filters,
                         kernel_size=filter_size,
                         padding='valid',
                         activation='relu',
                         strides=1,
                        input_shape=(sequence_length, embedding_dim)))

model.add(Dropout(dropout_prob[0]))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
model.add(Dropout(dropout_prob[1]))
model.add(Dense(hidden_dims, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])


print(model.summary())
print("Training model...")
model.fit(x_train, y_train, batch_size=batch_size, epochs=num_epochs,
validation_data=(x_test, y_test), verbose=2)




score = model.evaluate(x_test, y_test, verbose=0)

print("Accuracy: %.2f%%" % (score[1]*100))



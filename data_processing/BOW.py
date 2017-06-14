import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import  string
import nltk
import random
import pymorphy2

twtk = TweetTokenizer()

morph = pymorphy2.MorphAnalyzer(lang='uk')

classes = {"very good": 0, "good": 1, "uncertain": 2, "bad": 3, "very bad": 4 }
bigram_array = ["не", "дуже", "сильно", "навіть", "cправді", "найбільш" найменш мало безумовно безперечно ]


def read_from_file(filename):
    with open(filename, "r") as f:
        s = f.readlines()
        news = ''
        for stringg in s:
            news += stringg

        myjson = json.loads(news)
    return myjson

def process_tip(tip, stop_words, unique=True):

    words = [word.lower() for word in twtk.tokenize(tip) if word not in string.punctuation and word not in stop_words]
    for i in range(1, len(words)):
        if i - 1 == "не":
           words[i] = "не" + words[i]
        words[i] = morph.parse(words[i])[0].normal_form

    if unique:
        words = set(words)

    return words


def generate_ngrams(text):
    new_text = []
    index = 0
    while index != len(text):
        [new_word, new_index] = concatenate_words(index, text)
        new_text.append(new_word)
        index = new_index + 1 if index != new_index else index + 1
    return new_text


def concatenate_words(index, text):
    word = text[index]
    if index == len(text) - 1:
        return word, index
    if word in bigram_array:
        [word_new, new_index] = concatenate_words(index + 1, text)
        word = word + ' ' + word_new
        index = new_index
    return word, index

with open("/home/dzvinka/PycharmProjects/UkrTonalDict/dictionaries/ukrainian_stop_words", "r") as file:
    lines = file.readlines()
    ukr_stop_words = [word for word in lines]


tips = read_from_file("/home/dzvinka/PycharmProjects/UkrTonalDict/tips/sorted_reviews.json")


BOW = {}

for category in tips:
    for tip in tips[category]:
        for word in generate_ngrams(process_tip(tip, ukr_stop_words, unique=False)):
            if word not in BOW:
                BOW[word] = [0,0,0,0,0]
                BOW[word][classes[category]] += 1
            else:
                BOW[word][classes[category]] += 1

print(BOW)
print(len(BOW))

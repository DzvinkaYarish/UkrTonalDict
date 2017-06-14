import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import  string
import nltk
import random
import pymorphy2

twtk = TweetTokenizer()

morph = pymorphy2.MorphAnalyzer(lang='uk')

classes = {"very bad": 0, "bad": 1, "uncertain": 2, "good": 3, "very good": 4 }
bigram_array = ["не", "дуже", "сильно", "навіть", "cправді", "найбільш" "найменш",  "мало", "безсумнівно",  "безумовно",  "безперечно"
                "очевидно", "більш", "менш" ]

def get_sentiment(word):
    for i in range(5):
        if max(word[1]) == word[1][i]:
            return str(i - 2)


def read_from_file(filename):
    with open(filename, "r") as f:
        s = f.readlines()
        news = ''
        for stringg in s:
            news += stringg

        myjson = json.loads(news)
    return myjson

def process_tip(tip, stop_words, unique=True):

    words = [word.lower() for word in twtk.tokenize(tip) if word.strip() not in string.punctuation and word.strip() not in stop_words]
    for i in range(1, len(words)):
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
    ukr_stop_words = [word.strip() for word in lines]


tips = read_from_file("/home/dzvinka/PycharmProjects/UkrTonalDict/tips/sorted_reviews.json")


BOW = {}

for category in tips:
    count = 0
    for tip in tips[category]:
        if count > 400:
            break
        #for word in generate_ngrams(process_tip(tip, ukr_stop_words, unique=False)):
        for word in process_tip(tip, ukr_stop_words, unique=False):
            if word not in BOW:
                BOW[word] = [0,0,0,0,0]
                BOW[word][classes[category]] += 1
            else:
                BOW[word][classes[category]] += 1
        count += 1

print(BOW)
print(len(BOW))
items = list(BOW.items())
print(items)
items.sort(key=lambda x:sum(x[1]), reverse=True)


file = open("my_sentiment_dict.txt", "w")
for item in items:
    if sum(item[1]) > 20 and int(get_sentiment(item)) != 0:
        file.write(item[0] + ":" + get_sentiment(item) + "\n")

file.close()
import json
from nltk.tokenize import word_tokenize
import  string
import nltk
import random

def tip_features(tip, dict_fword):
    #TODO: try to include also count
    words = [word.lower() for sent in word_tokenize(tip) for word in sent if word not in word not in string.punctuation]
    for i in range(1, len(words)):
        if i - 1 == "не":
           words[i] = "не" + words[i]
    words = set(words)

    features = {}
    for w in dict_fword:
        features["contains %s" %w] = (w  in  words)
    return features

def read_from_file(filename):
    with open(filename, "r") as f:
        s = f.readlines()
        news = ''
        for stringg in s:
            news += stringg

        myjson = json.loads(news)
    return myjson

def extract_tips_text(venues_dict):
    return [tip["text"] for idd in venues_dict for tip in venues_dict[idd]["tips"] ]

#prepare data
json_lviv_tips = read_from_file("lviv_venues_tips.json")
json_ternopil_tips = read_from_file("ternopil_venues_tips.json")
json_chernivtsi_tips = read_from_file("chernivtsi_venues_tips.json")
json_kyiv_tips = read_from_file("kyiv_venues_tips.json")

dictionary = [word.lower() for sentence in (word_tokenize(tip["text"]) for idd in json_lviv_tips for tip in json_lviv_tips[idd]["tips"] ) for word in sentence if word not in string.punctuation]

for i in range(1, len(dictionary)):
    if i - 1 == "не":
        dictionary[i] = "не" + dictionary[i]

dict_words = nltk.FreqDist(dictionary)
print(len(dict_words))
uneven_feature_set = [(tip_features(tip["text"], list(dict_words.keys())[:4000]), tip["authorInteractionType"]) for idd in json_lviv_tips for tip in json_lviv_tips[idd]["tips"]]
uneven_feature_set.extend([(tip_features(tip["text"], list(dict_words.keys())[:4000]), tip["authorInteractionType"]) for idd in json_ternopil_tips for tip in json_ternopil_tips[idd]["tips"]])
uneven_feature_set.extend([(tip_features(tip["text"], list(dict_words.keys())[:4000]), tip["authorInteractionType"]) for idd in json_chernivtsi_tips for tip in json_chernivtsi_tips[idd]["tips"]])
uneven_feature_set.extend([(tip_features(tip["text"], list(dict_words.keys())[:4000]), tip["authorInteractionType"]) for idd in json_kyiv_tips for tip in json_kyiv_tips[idd]["tips"]])
#uneven_feature_set.extend([(tip_features(tip["text"], list(dict_words.keys())[:4000]), tip["authorInteractionType"]) for idd in json_chernivtsi_tips for tip in json_chernivtsi_tips[idd]["tips"]])

fair_feature_set = []
i = 0
while (len(fair_feature_set) != 500):
    if uneven_feature_set[i][1] == "liked":
        fair_feature_set.append(uneven_feature_set[i])
    i+=1
i = 0
while (len(fair_feature_set) != 790):
    if uneven_feature_set[i][1] == "disliked":
        fair_feature_set.append(uneven_feature_set[i])
    i+=1
i=0
while (len(fair_feature_set) !=1121):
    if uneven_feature_set[i][1] == "meh":
        fair_feature_set.append(uneven_feature_set[i])
    i+=1
random.shuffle(fair_feature_set)

# count = 0
# for feature in uneven_feature_set:
#     if feature[1] == "disliked":
#         count += 1
# print(count)

train_set, test_set = fair_feature_set[100:], fair_feature_set[:100]



#train model
classifier = nltk.NaiveBayesClassifier.train(train_set)

#test model
print("accuracy %s" %str(nltk.classify.accuracy(classifier, test_set)))
print(classifier.classify(
    tip_features("Фірмове пиво не сподобалось. Несмачне. Загалом в закладі погано. Часом важко пересуватись між столиками.",list(dict_words.keys())[:3000])))

classifier.show_most_informative_features(20)


dev_set = [(tip["text"], tip["authorInteractionType"]) for idd in json_ternopil_tips for tip in json_ternopil_tips[idd]["tips"]]

errors = []
for (tip, label) in dev_set[:100]:
    guess = classifier.classify(tip_features(tip, list(dict_words.keys())[:4000]))
    if (guess != label):
        errors.append((label, guess, tip))

for (label, guess, tip) in errors:
    print('correct=%-8s guess=%-8s text=%-30s' %(label, guess, tip))

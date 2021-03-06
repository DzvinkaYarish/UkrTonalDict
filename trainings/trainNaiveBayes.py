import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import  string
import nltk
import random
import pymorphy2
import pickle
import sys


twtk = TweetTokenizer()

morph = pymorphy2.MorphAnalyzer(lang='uk')

numb_of_words_dict = 2000


def tip_features(words, dict_fword):
    #TODO: try to include also count
    #words = [word.lower() for sent in word_tokenize(tip) for word in sent if word not in word not in string.punctuation]
    features = {}
    for w in dict_fword:
        features["contains %s" %w] = (w  in  words)
    return features


def process_tip(tip, stop_words, unique=True):
    words = [word.lower() for word in twtk.tokenize(tip) if word.isalpha() and word.strip() not in stop_words]
    adjectives = []
    for i in range(0, len(words)):
        adj = False
        parsers = morph.parse(words[i])
        for parse in parsers:

            if ('ADJF' in parse.tag or 'ADVB' in parse.tag) and not adj:
                adjectives.append(parse.normal_form)
                adj = True

    if unique:
        adjectives = set(adjectives)

    return adjectives




def read_from_file(filename):
    with open(filename, "r") as f:
        s = f.readlines()
        news = ''
        for stringg in s:
            news += stringg

        myjson = json.loads(news)
    return myjson




if __name__ == "__main__" :
    #prepare data
    with open("ukrainian_stop_words", "r") as file:
        lines = file.readlines()
        ukr_stop_words = [word.strip() for word in lines]


    #print(process_tip("Фірмове пиво не сподобалось. Несмачне. Загалом в закладі погано. Часом важко пересуватись між столиками.", ukr_stop_words))






    json_tips = read_from_file("sorted_reviews.json")
    json_odesa_tips = read_from_file("odesa_venues_tips.json")


    dictionary = []

    for type in json_tips:
        count = 0
        for tip in json_tips[type]:
            dictionary.extend(process_tip(tip, ukr_stop_words, unique=False))
            count += 1
            if count > 600:
                break


    dict_words = nltk.FreqDist(dictionary)
    dict_most_freq = [word[0]for word in dict_words.most_common(numb_of_words_dict)]


    feature_set_good = [(tip_features(process_tip(tip, ukr_stop_words), dict_most_freq), "very good") for tip in json_tips["good"]]  # numb of features - 5428
    feature_set_uncertain  = [(tip_features(process_tip(tip, ukr_stop_words), dict_most_freq), "uncertain") for tip in json_tips["uncertain"]] # numb of features - 398
    feature_set_bad = [(tip_features(process_tip(tip, ukr_stop_words), dict_most_freq), "very bad") for tip in json_tips["bad"]] #numb of features - 516

    feature_set_very_bad = [(tip_features(process_tip(tip, ukr_stop_words), dict_most_freq), "bad") for tip in json_tips["very bad"]] #numb of features - 516
    feature_set_very_good = [(tip_features(process_tip(tip, ukr_stop_words), dict_most_freq), "good") for tip in json_tips["very good"]] #numb of features - 516


    random.shuffle(feature_set_good)
    random.shuffle(feature_set_very_good)
    random.shuffle(feature_set_very_bad)
    random.shuffle(feature_set_uncertain)
    random.shuffle(feature_set_bad)


    fair_feature_set = []
    test_set = []
    fair_feature_set.extend(feature_set_good[:400])
    test_set.extend(feature_set_good[400:425])

    #fair_feature_set.extend(feature_set_uncertain[:398])
    fair_feature_set.extend(feature_set_bad[:340])
    test_set.extend(feature_set_bad[340:360])



    fair_feature_set.extend(feature_set_very_bad[:340])
    test_set.extend(feature_set_very_bad[340:360])

    fair_feature_set.extend(feature_set_very_good[:400])
    test_set.extend(feature_set_very_good[400:425])



    random.shuffle(fair_feature_set)


    train_set = fair_feature_set



    #train model
    classifier = nltk.NaiveBayesClassifier.train(train_set)

    #test model
    print("accuracy %s" %str(nltk.classify.accuracy(classifier, test_set)))
    print(classifier.classify(
        tip_features("Фірмове пиво не сподобалось. Несмачне. Загалом в закладі погано. Часом важко пересуватись між столиками.",list(dict_words.keys())[:3000])))

    classifier.show_most_informative_features(20)


    dev_set = [(tip["text"], tip["authorInteractionType"]) for idd in json_odesa_tips for tip in json_odesa_tips[idd]["tips"]]

    #random.shuffle(fair_feature_set)
    #dev_set = fair_feature_set[:100]
    errors = []
    for (tip, label) in dev_set:
        guess = classifier.classify(tip_features(process_tip(tip, ukr_stop_words), dict_most_freq))
        #guess = classifier.classify(tip)
        #if (guess != label):
        errors.append((label, guess, tip))

    for (label, guess, tip) in errors:
        print('correct=%-8s guess=%-8s text=%-30s' %(label, guess, tip))

    accuracy = str(nltk.classify.accuracy(classifier, test_set))
    print("accuracy %s" % accuracy)
    print(classifier.classify(

            tip_features(process_tip(
                "Фірмове пиво не сподобалось. Несмачне. Загалом в закладі погано. Часом важко пересуватись між столиками.", ukr_stop_words),
                dict_most_freq)))
    print(process_tip("Фірмове пиво не сподобалось. Несмачне. Загалом в закладі погано. Часом важко пересуватись між столиками.", ukr_stop_words))


    if float(sys.argv[1]) <  float(accuracy):
        print("save model to file")
        f = open('my_classifier_4.pickle', 'wb')
        pickle.dump(classifier, f)
        f.close()


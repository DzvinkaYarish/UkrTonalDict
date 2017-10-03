from models import Place, Base, Review
from sqlalchemy import create_engine
from nltk.tokenize import TweetTokenizer
import pymorphy2, string


twtk = TweetTokenizer()

morph = pymorphy2.MorphAnalyzer(lang='uk')
import csv

engine = create_engine('sqlite:///ukrainian.db')
Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker


DBSession = sessionmaker()
DBSession.bind = engine

session = DBSession()

reviews = session.query(Review).all()

with open("../tips/ukrainian_lemmatized.csv", "w") as f:
    writer = csv.writer(f, delimiter='|')
    writer.writerow(["opinion_text", "opinion_rating"])
    for rvw in reviews:
        words = [word.lower() for word in twtk.tokenize(rvw.text) if
                 word not in string.punctuation]
        for i in range(1, len(words)):

            if i - 1 == "не":
                words[i] = "не" + words[i]
            words[i] = morph.parse(words[i])[0].normal_form

        writer.writerow([" ".join(words), rvw.sentiment])




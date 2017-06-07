

import json
from polyglot.detect import Detector, base


def read_from_file(filename):
    with open(filename, "r") as f:
        s = f.readlines()
        news = ''
        for stringg in s:
            news += stringg

        myjson = json.loads(news)
    return myjson


fb_reviews = read_from_file("facebook_rewiews.json")



ukr_fb_reviews = {}
count_ukr = 0
count = 0

for venue in fb_reviews:
    for tip in fb_reviews[venue]:
        count += 1
        try:
            lang_detector = Detector(tip[2])
            ukr = lang_detector.language.name == "Ukrainian"
        except base.UnknownLanguage:
            continue
        if ukr:
            count_ukr += 1
            if venue in ukr_fb_reviews.keys():
                ukr_fb_reviews[venue].append(tip)
            else:
                ukr_fb_reviews[venue] = [tip]

print(count)
print(count_ukr)



with open("ukr_fb_rewiews.json", "w") as file:
    file.write(json.dumps(ukr_fb_reviews, ensure_ascii=False))



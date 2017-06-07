

import json
#from polyglot.detect import Detector, base


def read_from_file(filename):
    with open(filename, "r") as f:
        s = f.readlines()
        news = ''
        for stringg in s:
            news += stringg

        myjson = json.loads(news)
    return myjson


fb_reviews = read_from_file("ukr_fb_rewiews.json")

good_rewiews = []
bad_rewiews = []
uncertain_rewiews = []



for venue in fb_reviews:
    for tip in fb_reviews[venue]:
        if tip[3] == "5 star" or tip[3] == "4 star":
            good_rewiews.append(tip[2])
        elif tip[3] == "3 star":
            uncertain_rewiews.append(tip[2])
        else:
            bad_rewiews.append(tip[2])


forsquare_rew = read_from_file("all_venues_tips.json")

for idd in forsquare_rew:
    for tip in forsquare_rew[idd]["tips"]:
        if tip["authorInteractionType"] == "liked":
            good_rewiews.append(tip["text"])
        elif tip["authorInteractionType"] == "meh":
            uncertain_rewiews.append(tip["text"])
        else:
            bad_rewiews.append(tip["text"])


all_reviews = {"good":good_rewiews, "uncertain": uncertain_rewiews,"bad": bad_rewiews}

print(len(good_rewiews))
print(len(uncertain_rewiews))
print(len(bad_rewiews))


with open("sorted_reviews.json", "w") as file:
    file.write(json.dumps(all_reviews, ensure_ascii=False))



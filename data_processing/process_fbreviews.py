

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


fb_reviews = read_from_file("tips/ukr_fb_rewiews.json")

very_good_rewiews = []
very_bad_rewiews = []
good_rewiews = []
bad_rewiews = []
uncertain_rewiews = []


count = 0
for venue in fb_reviews:
    for tip in fb_reviews[venue]:
        count += 1
        if tip[3] == "4 star":
            print("good feview")
            good_rewiews.append(tip[2])
        elif tip[3] == "5 star":
            very_good_rewiews.append(tip[2])
        elif tip[3] == "3 star":
            uncertain_rewiews.append(tip[2])
        elif tip[3] == "2 star":
            bad_rewiews.append(tip[2])
        else:
            very_bad_rewiews.append(tip[2])

print("fb " + str(count))

count = 0
forsquare_rew = read_from_file("tips/all_venues_tips.json")

for idd in forsquare_rew:

    for tip in forsquare_rew[idd]["tips"]:
        count += 1
        if tip["authorInteractionType"] == "liked" and tip["agreeCount:"] > 0:
            very_good_rewiews.append(tip["text"])
        elif tip["authorInteractionType"] == "disliked" and tip["agreeCount:"] > 0:
            very_bad_rewiews.append(tip["text"])
        elif tip["authorInteractionType"] == "liked":
            good_rewiews.append(tip["text"])
        elif tip["authorInteractionType"] == "disliked":
            bad_rewiews.append(tip["text"])
        else:
            uncertain_rewiews.append(tip["text"])

print("fr: "+ str(count))
all_reviews = {"good":good_rewiews, "uncertain": uncertain_rewiews,"bad": bad_rewiews, "very good": very_good_rewiews, "very bad": very_bad_rewiews}

print(len(good_rewiews))
print(len(uncertain_rewiews))
print(len(bad_rewiews))
print()

print(len(very_good_rewiews))
print(len(very_bad_rewiews))


with open("tips/sorted_reviews.json", "w") as file:
    file.write(json.dumps(all_reviews, ensure_ascii=False))



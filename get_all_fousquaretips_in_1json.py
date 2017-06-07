import json
from trainNaiveBayes import read_from_file

all_venues = {}

for file in (["tips/lviv_venues_tips.json", "tips/ternopil_venues_tips.json", "tips/chernivtsi_venues_tips.json", "tips/kyiv_venues_tips.json", "tips/lutsk_venues_tips.json", "tips/odesa_venues_tips.json"]):
    myjson = read_from_file(file)
    print(len(list(myjson.keys())))
    for id in myjson:
        if id in all_venues:
            all_venues[id]["tips"].extend(myjson[id]["tips"])
        else:
            all_venues[id] = myjson[id]

print(len(list(all_venues.keys())))


with open("all_venues_tips.json", "w") as file:
    file.write(json.dumps(all_venues, ensure_ascii=False))



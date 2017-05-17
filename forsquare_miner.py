import urllib.request, urllib.parse
import json
from olesforsquareminer import get_tips
from polyglot.detect import Detector, base
from settings import CLIENT_ID, CLIENT_SECRET



venues = {}
latitude = 49.80
longitude = 23.88
url = "https://api.foursquare.com/v2/venues/explore"
#"ll":str(latitude) + "," + str(longitude)
count_tips = 0

for i in range(199):
    data = urllib.parse.urlencode(
                {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "near":"Chernivtsi, UA", "v":"20170515", "radius": "10000",
                 "intent":"chekin", "limit":"50", "openNow":"0", "saved":"0", "specials":"0", "offset":i})

    x = urllib.request.urlopen(url + "?" + data)


    items = json.loads(x.read().decode("utf-8"))["response"]["groups"][0]["items"]

    for k in range(len(items)):
        venue = items[k]["venue"]
        if venue["id"] not in venues.keys():

            tips = get_tips(venue["id"])
            if (tips):
                venue_dict = {"name":str(venue["name"]), "tips":[]}

                for tip in tips:
                    ukr = False
                    if ('authorInteractionType' in tip):
                        if ("lang" in tip):
                            ukr = tip["lang"] == "uk"

                        else:
                            try:
                                lang_detector = Detector(tip['text'])
                                ukr = lang_detector.language.name == "Ukrainian"
                            except base.UnknownLanguage:
                                continue
                            # print(lang_detector.language.name)
                            # print('text: ', tip['text'])
                            # print('authorInteractionType:', tip['authorInteractionType'])
                            # print('agreeCount:', tip['agreeCount'])
                            # print('disagreeCount', tip['disagreeCount'])
                        if ukr:
                            count_tips += 1
                            tip_dict = {'text': str(tip['text']), 'authorInteractionType': tip['authorInteractionType'],
                                        'agreeCount:': tip['agreeCount'], 'disagreeCount': tip['disagreeCount']}
                            venue_dict["tips"].append(tip_dict)
                if (venue_dict["tips"]):
                    #print("id: ", venue["id"])
                    print("name: ", venue["name"])
                    venues[venue["id"]] = venue_dict
                    #print(venue_dict)


print(len(list(venues.keys())))
print(count_tips)
with open("chernivtsi_venues_tips.json", "w") as file:
    file.write(json.dumps(venues, ensure_ascii=False))

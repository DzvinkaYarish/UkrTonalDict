import urllib.request, urllib.parse
import json
from forsquareminer import get_tips
from polyglot.detect import Detector, base

CLIENT_ID = "44G2WRBSKTTKKKEB4E1C5IECVUVSXCFAXDLFVWRQXAI0KQHU"
CLIENT_SECRET = "AJMPTFLXKUHSNO2D1QI1C5LAD3LFOPUMDGPZGRRENJGF3TYP"

#OAUTH_TOKEN =
venues = {"venues": []}
latitude = 49.80
longitude = 23.88
url = "https://api.foursquare.com/v2/venues/explore"
#"ll":str(latitude) + "," + str(longitude)
#near":"Lviv, UA",

for i in range(11):
    data = urllib.parse.urlencode(
                {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "near":"Lviv, UA", "v":"20170515", "radius": "10000",
                 "intent":"chekin", "limit":"50", "openNow":"0", "saved":"0", "specials":"0", "offset":i})

    x = urllib.request.urlopen(url + "?" + data)
    #print(url + "?" + data)

    items = json.loads(x.read().decode("utf-8"))["response"]["groups"][0]["items"]
    for k in range(len(items)):
        venue = items[k]["venue"]
        tips = get_tips(venue["id"])

        if (tips):
            venue_dict = {"id": venue["id"], "name":venue["name"], "tips":[]}
            print("id: ", venue["id"])
            print("name: ", venue["name"])
            for tip in tips:


                if ('authorInteractionType' in tip):

                    #and lang_detector.language.name == "Ukrainian"): # and lang ukr :
                    try:
                        lang_detector = Detector(tip['text'])
                    except base.UnknownLanguage:
                        continue
                    if tip["lang"] == "uk" or lang_detector.language.name == "Ukrainian" :
                        # print(lang_detector.language.name)
                        # print('text: ', tip['text'])
                        # print('authorInteractionType:', tip['authorInteractionType'])
                        # print('agreeCount:', tip['agreeCount'])
                        # print('disagreeCount', tip['disagreeCount'])
                        tip_dict = {'text': tip['text'], 'authorInteractionType': tip['authorInteractionType'],
                                    'agreeCount:': tip['agreeCount'], 'disagreeCount': tip['disagreeCount']}
                        venue_dict["tips"].append(tip_dict)
            if (venue_dict["tips"]):
                venues["venues"].append(venue_dict)



my_json = json.dumps(venues)
with open("lviv_venues_tips.json", "w") as file:
    file.write(my_json)

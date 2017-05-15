import urllib.request, urllib.parse
import json
from forsquareminer import get_tips
from polyglot.detect import Detector, base

CLIENT_ID = "44G2WRBSKTTKKKEB4E1C5IECVUVSXCFAXDLFVWRQXAI0KQHU"
CLIENT_SECRET = "AJMPTFLXKUHSNO2D1QI1C5LAD3LFOPUMDGPZGRRENJGF3TYP"

#OAUTH_TOKEN =
global_venues = []
latitude = 49.80
longitude = 23.88
url = "https://api.foursquare.com/v2/venues/explore"
#
#near":"Lviv, UA",

for i in range(4):
    for j in range(14):

        data = urllib.parse.urlencode(
                {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "ll":str(latitude) + "," + str(longitude), "v":"20170515", "radius": "1000",
                 "intent":"chekin", "limit":"5", "openNow":"0", "saved":"0", "specials":"0", "offset":"1"})

        x = urllib.request.urlopen(url + "?" + data)

        items = json.loads(x.read().decode("utf-8"))["response"]["groups"][0]["items"]
        for k in range(len(items)):
            count = 0
            venue = items[k]["venue"]
            tips = get_tips(venue["id"])
            if (tips) and (venue["id"] not in global_venues):
                global_venues.append(venue["id"])
                print("id: ", venue["id"])
                print("name: ", venue["name"])

                count += 1
                for tip in tips:

                    if ('authorInteractionType' in tip):
                        #and lang_detector.language.name == "Ukrainian"): # and lang ukr :
                        try:
                            lang_detector = Detector(tip['text'])
                        except base.UnknownLanguage:
                            continue
                        print(lang_detector.language.name)
                        print('text: ', tip['text'])
                        print('authorInteractionType:', tip['authorInteractionType'])
                        print('agreeCount:', tip['agreeCount'])
                        print('disagreeCount', tip['disagreeCount'])
            print(count)
        longitude += 0.01
    latitude += 0.01

print(len(global_venues))



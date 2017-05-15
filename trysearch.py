import urllib.request, urllib.parse
import json
from forsquareminer import get_tips
from polyglot.detect import Detector

CLIENT_ID = "44G2WRBSKTTKKKEB4E1C5IECVUVSXCFAXDLFVWRQXAI0KQHU"
CLIENT_SECRET = "AJMPTFLXKUHSNO2D1QI1C5LAD3LFOPUMDGPZGRRENJGF3TYP"

#OAUTH_TOKEN =
global_venues = []
latitude = 49.76
longitude = 23.88
url = "https://api.foursquare.com/v2/venues/search"

for i in range(4):
    for j in range(14):

        data = urllib.parse.urlencode(
                {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "ll":str(latitude) + "," + str(longitude), "v":"20170515", "radius": "50", "intent":"chekin", "limit":"30"})

        x = urllib.request.urlopen(url + "?" + data)

        venues = json.loads(x.read().decode("utf-8"))["response"]["venues"]
        count = 0
        for venue in venues:
            tips = get_tips(venue["id"])
            if (tips) and (venue["id"] not in global_venues):
                global_venues.append(venue["id"])
                print("id: ", venue["id"])
                print("name: ", venue["name"])

                count += 1
                for tip in tips:
                    lang_detector = Detector(tip['text'])
                    if ('authorInteractionType' in tip and lang_detector.language.name == "Ukrainian"): # and lang ukr :
                        print('text: ', tip['text'])
                        print('authorInteractionType:', tip['authorInteractionType'])
                        print('agreeCount:', tip['agreeCount'])
                        print('disagreeCount', tip['disagreeCount'])
        print(count)
        longitude += 0.02
    latitude += 0.02

print(len(global_venues))



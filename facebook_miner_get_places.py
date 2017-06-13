import urllib.request, urllib.parse
import json

FACEBOOK_ACCESS_TOKEN = "680740112135077%7CEq_CUNKKEzblfj8bkkn6GtKV1cI"
def get_places():
    url ="https://graph.facebook.com/v2.9/search"
    # list of all fields https://developers.facebook.com/docs/places/fields
    #"49.8397,24.0297"

    parsed_data = {}


    for k in range(2):
        lat = 49.8397
        longit = 24.0297
        for i in range(20):
            for j in range(20):


                coord = str(lat) + "," + str(longit)
                args = urllib.parse.urlencode({"type": "place", "center": coord, "distance": "1100", "fields": "name,checkins,picture", "access_token": FACEBOOK_ACCESS_TOKEN, "limit":100
            })
                #print(url + "?" + args)
                x = urllib.request.urlopen(url + "?" + args)
                data = json.loads(x.read().decode("utf-8"))['data']


                for place in data:
                    parsed_data[place['name']] = 'https://www.facebook.com/pg/%s/reviews/' % place['id']

                if (k == 0):

                    longit += 0.005
                else:
                    longit -= 0.005
            if k == 0:
                lat += 0.005
            else:
                lat -= 0.005




    return parsed_data

places = get_places()
print(places)
print(len(places))

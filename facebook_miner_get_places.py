import urllib.request, urllib.parse
import json

FACEBOOK_ACCESS_TOKEN = "680740112135077%7CEq_CUNKKEzblfj8bkkn6GtKV1cI"
def get_places():
    url ="https://graph.facebook.com/v2.9/search"
    # list of all fields https://developers.facebook.com/docs/places/fields
    args = urllib.parse.urlencode({"type": "place", "center": "49.8397,24.0297", "distance": "1000", "fields": "name,checkins,picture", "access_token": FACEBOOK_ACCESS_TOKEN, "limit":100
})
    print(url + "?" + args)
    x = urllib.request.urlopen(url + "?" + args)
    data = json.loads(x.read().decode("utf-8"))['data']
    parsed_data = {}

    for place in data:
        parsed_data[place['name']] = 'https://www.facebook.com/pg/%s/reviews/' % place['id']

    return parsed_data

places = get_places()
print(places)
print(len(places))

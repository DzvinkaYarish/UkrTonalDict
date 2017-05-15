import urllib.request, urllib.parse
import json

CLIENT_ID = "44G2WRBSKTTKKKEB4E1C5IECVUVSXCFAXDLFVWRQXAI0KQHU"
CLIENT_SECRET = "AJMPTFLXKUHSNO2D1QI1C5LAD3LFOPUMDGPZGRRENJGF3TYP"

def get_tips(venue_id):
    """
    https://api.foursquare.com/v2/venues/VENUE_ID/tips
    """
    url = "https://api.foursquare.com/v2/venues/%s/tips" % venue_id

    data = urllib.parse.urlencode({"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "sort": "recent", "v": "20170510", "limit":"500", "offset":"1"})
    x = urllib.request.urlopen(url + "?" + data)
    x = x.read().decode("utf-8")
    return json.loads(x)['response']['tips']['items']

#tips = json.loads(get_tips("54b69c3a498e7aea12b2bba9"))['response']['tips']['items']

# for tip in tips:
#     if 'authorInteractionType' in tip:
#         print('text: ', tip['text'])
#         print('authorInteractionType:', tip['authorInteractionType'])
#         print('agreeCount:', tip['agreeCount'])
#         print('disagreeCount', tip['disagreeCount'])
#         print()

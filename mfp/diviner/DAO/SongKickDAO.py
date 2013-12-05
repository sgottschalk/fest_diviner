import requests

from diviner.models import VenueInformation, EventInformation

apiKey = 'ipBxS0KlUqMwcdST'


# TODO: pagination
def getConcertsForArtist(**kwargs):
    # Build the request
    artistPathTerm = ('mbid:' + kwargs.get('mbid')) if ('mbid' in kwargs) else (kwargs.get('songkickid'))
    requestUrl = 'http://api.songkick.com/api/3.0/artists/%s/calendar.json' % artistPathTerm
    requestParams = {
        'apikey': apiKey,
        'min_date': kwargs.get('minDate'),
        'max_date': kwargs.get('maxDate')
    }

    # Retrieve and parse the response
    response = requests.get(requestUrl, params=requestParams)
    print response.url
    json = response.json()['resultsPage']
    if json['status'] != 'ok':
        return None
    concerts = []
    if json['totalEntries'] == 0:
        return concerts
    # Go over each event and add it to the concerts list
    for event in json['results']['event']:
        locObj = event['location']
        venueObj = event['venue']
        venueInfo = VenueInformation(locObj['lat'], locObj['lng'], locObj['city'], venueObj['displayName'])
        eventInfo = EventInformation(event['start']['date'], venueInfo)
        concerts.append(eventInfo)
    return concerts

# messing around
# print getConcertsForArtist(mbid = '50601ad0-50e5-40ae-b446-d6ada5986d19', minDate = '2014-05-20', maxDate = '2014-05-30')
# print getConcertsForArtist(songkickid = '503872', minDate = '2014-05-20', maxDate = '2014-05-30')
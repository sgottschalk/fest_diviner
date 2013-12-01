import requests

from diviner.models import VenueInformation, EventInformation

apiKey = 'ipBxS0KlUqMwcdST'

# TODO: start and end date filtering on the result set
# TODO: change this to kwargs so that either mbid or songkickid can be passed
# TODO: pagination
def getConcertsForArtist(mbid):
    response = requests.get(('http://api.songkick.com/api/3.0/artists/mbid:%s/calendar.json') % (mbid), params = {'apikey': apiKey})
    json = response.json()['resultsPage']
    if json['status'] != 'ok':
        return None
    concerts = []
    for event in json['results']['event']:
        venueInfo = VenueInformation(event['location']['lat'], event['location']['lng'], event['location']['city'], event['venue']['displayName'])
        eventInfo = EventInformation(event['start']['date'], venueInfo)
        concerts.append(eventInfo)
    return concerts
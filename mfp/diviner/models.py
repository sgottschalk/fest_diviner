import datetime
from dateutil import parser
from django.db import models


#############################
# Database models
#############################
from diviner.utilities import Constants
from diviner.utilities.Constants import DailyStatus
from diviner.utilities import CacheHelpers
from diviner.utilities import GeneralUtils
from diviner.utilities import LocationUtils


class Festival(models.Model):
    """
    Model representing a particular festival.
    The url field dictates the relative url for the festival off of /festivals.
    """
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=20, unique=True)
    lat = models.FloatField()
    lng = models.FloatField()
    venue_id = models.CharField(max_length=10)
    
    def __unicode__(self):
        return u'[name: %s, url: %s, lat: %s, lng: %s, venue_id: %s]' % \
               (self.name, self.url, self.lat, self.lng, self.venue_id)


class FestDate(models.Model):
    """
    Model representing a day for a festival.
    """
    festival = models.ForeignKey(Festival)
    day = models.DateField()

    def __unicode__(self):
        return u'[festival: %s, day: %s]' % (self.festival, self.day)

    # TODO: db doesn't reflect this yet, so leave it out
    # class Meta:
    #     unique_together = ('festival', 'day')


class Artist(models.Model):
    """
    Model representing an artist that is being tracked for a festival.
    """
    mbid = models.CharField(max_length=36, unique=True, null=True)
    songkickid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    festival = models.ForeignKey(Festival)
    statuses = None

    def adornStatusPerDay(self):
        dates = self.festival.festdate_set.dates('day', 'day', order='ASC')
        startDate = dates[0]
        endDate = dates.reverse()[0]
        dayBuffer = datetime.timedelta(days=3)
        concerts = self.getConcertsForArtist(minDate=startDate - dayBuffer, maxDate=endDate + dayBuffer)
        self.statuses = []
        # Heavy lifting portion
        for festDate in dates:
            # TODO: do this in a smarter way, processors maybe?
            # First check if the artist is booked on any of the festival days
            if festDate in concerts:
                if concerts[festDate].venueInformation.venueId is self.festival.venue_id:
                    self.statuses.append(DailyStatus.YES)
                else:
                    self.statuses.append(DailyStatus.NO)
            else:
                # TODO: See if sasquatch fits into their tour schedule
                self.statuses.append(self.findPreviousAndNextConcert(concerts, festDate))
                # self.statuses.append(DailyStatus.MAYBE)
        # Check if it fits into tour schedule
        self.parseConcerts(concerts)
        return self

    def findPreviousAndNextConcert(self, concerts, festDate):
        """
        Checks the alignment of previously scheduled concerts against festDate.

        :param concerts: Already scheduled concerts around the festival dates
        :param festDate: The particular day to compare with
        :return: A DailyStatus
        """
        if not concerts:
            return DailyStatus.MAYBE
        concertDates = concerts.keys()
        concertDates.sort()

        insertionPt = GeneralUtils.binary_search(concertDates, festDate)

        # first check edge cases
        if insertionPt == len(concertDates) or insertionPt == 0:
            index = (insertionPt - 1) if (insertionPt == len(concertDates)) else insertionPt
            concertInfoBefore = concerts.get(concertDates[index]).venueInformation
            daysBetween = abs((concertDates[index] - festDate).days)
            distanceBetween = LocationUtils.haversine(concertInfoBefore.lat, concertInfoBefore.lng, self.festival.lat, self.festival.lng)
            if distanceBetween < (Constants.haversineDistancePaddingPerDay * daysBetween):
                return DailyStatus.PROBABLE
            else:
                return DailyStatus.MAYBE
        else:
            # This date is sandwiched between other dates
            concertInfoBefore = concerts.get(concertDates[insertionPt - 1]).venueInformation
            concertInfoAfter = concerts.get(concertDates[insertionPt]).venueInformation
            # distance from previous concert to festival
            distanceToFestival = LocationUtils.haversine(concertInfoBefore.lat, concertInfoBefore.lng, self.festival.lat, self.festival.lng)
            # distance from festival to next concert
            distanceFromFestival = LocationUtils.haversine(self.festival.lat, self.festival.lng, concertInfoAfter.lat, concertInfoAfter.lng)
            # distance from previous concert to next concert
            distanceNoFestival = LocationUtils.haversine(concertInfoBefore.lat, concertInfoBefore.lng, concertInfoAfter.lat, concertInfoAfter.lng)
            # TODO: Currently it doesn't take into account the days between like the above case
            if (distanceToFestival + distanceFromFestival) < (distanceNoFestival + Constants.haversineDistancePaddingPerDay):
                return DailyStatus.PROBABLE
            else:
                return DailyStatus.MAYBE

    def parseConcerts(self, concerts):
        # LocationUtils.haversine(lat1, lng1, lat2, lng2)
        pass

    def getConcertsForArtist(self, **kwargs):
        """
        Returns a map of date->concert for the given artist between the given dates.

        Keyword Arguments:
        minDate -- minimum date to request (required)
        maxDate -- maximum date to request (required)
        """
        # Build the request
        artistPathTerm = ('mbid:' + self.mbid) if (self.mbid is not None) else self.songkickid
        requestUrl = 'http://api.songkick.com/api/3.0/artists/%s/calendar.json' % artistPathTerm
        requestParams = {
            'apikey': Constants.songKickApiKey,
            'min_date': kwargs.get('minDate'),
            'max_date': kwargs.get('maxDate')
        }

        # Retrieve and parse the response
        response = CacheHelpers.retrieveRequestJson(requestUrl, requestParams)
        # print response.url
        json = response['resultsPage']
        if json['status'] != 'ok':
            return None
        concerts = {}
        if json['totalEntries'] == 0:
            return concerts
        # Go over each event and add it to the concerts list
        for event in json['results']['event']:
            locObj = event['location']
            venueObj = event['venue']
            venueInfo = VenueInformation(locObj['lat'],
                                         locObj['lng'],
                                         locObj['city'],
                                         venueObj['displayName'],
                                         venueObj['id'])
            eventDate = parser.parse(event['start']['date']).date()
            eventInfo = EventInformation(eventDate, venueInfo)
            concerts[eventDate] = eventInfo
        return concerts

    def __unicode__(self): 
        return u'[mbid: %s, songkickid: %s, name: %s, festival: %s, statuses: %s]' % \
               (self.mbid, self.songkickid, self.name, self.festival, str(self.statuses))


#############################
# Application models
#############################
class MusicBrainzArtist():
    mbid = None
    name = None
    
    def __init__(self, mbid, name):
        self.mbid = mbid
        self.name = name
        
    def __unicode__(self):
        return u'[mbid: %s, name: %s]' % (self.mbid, self.name)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()


class ArtistEventInformation():
    mbid = None
    songkickid = None
    name = None
    events = None
    
    def __init__(self, mbid, songkickid, name, events):
        self.mbid = mbid
        self.songkickid = songkickid
        self.name = name
        self.events = events
        
    def __unicode__(self):
        return u'[mbid: %s, songkickid: %s, name: %s, events: %s]' % \
               (self.mbid, self.songkickid, self.name, self.events)


class EventInformation():
    date = None
    venueInformation = None

    def __init__(self, date, venueInformation):
        self.date = date
        self.venueInformation = venueInformation

    def __unicode__(self):
        return u'[date: %s, venueInformation: %s]' % (self.date, self.venueInformation)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()


class VenueInformation():
    lat = None
    lng = None
    city = None
    venueName = None
    venueId = None

    def __init__(self, lat, lng, city, venueName, venueId):
        self.lat = lat
        self.lng = lng
        self.city = city
        self.venueName = venueName
        self.venueId = venueId

    def __unicode__(self):
        return u'[lat: %s, lng: %s, city: %s, venueName: %s, venueId: %s]' \
               % (self.lat, self.lng, self.city, self.venueName, self.venueId)

    def __str__(self):
        return self.__unicode__()

    def __repr__(self):
        return self.__unicode__()


class ArtistSearchResult():
    displayName = None
    songkickId = None

    def __init__(self, displayName, songkickId):
        self.displayName = displayName
        self.songkickId = songkickId


class ArtistSearch():
    """
    Model that takes a artist search string and returns a list of ArtistSearchResult models.
    """
    searchString = None

    def __init__(self, searchString):
        self.searchString = searchString

    def executeSearch(self):
        # Build the request
        requestUrl = 'http://api.songkick.com/api/3.0/search/artists.json'
        requestParams = {
            'apikey': Constants.songKickApiKey,
            'query': self.searchString,
            'per_page': Constants.artistSearchResultNumber
        }

        # Retrieve and parse the response
        response = CacheHelpers.retrieveRequestJson(requestUrl, requestParams)
        searchResults = response['resultsPage']
        if searchResults['status'] != 'ok':
            return None
        results = []
        if searchResults['totalEntries'] == 0:
            return results
        for result in searchResults['results']['artist']:
            mbid = None
            if result['identifier'] != []:
                # TODO: Always take the first element?
                mbid = result['identifier'][0]['mbid']
            results.append(ArtistSearchResult(result['displayName'], result['id']))
        return results
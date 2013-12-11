import datetime
from dateutil import parser
from django.db import models
import requests


#############################
# Database models
#############################
from diviner.utilities import Constants
from diviner.utilities.Constants import DailyStatus


class Festival(models.Model):
    """
    Model representing a particular festival.
    The url field dictates the relative url for the festival off of /festivals.
    """
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=20, unique=True)
    lat = models.FloatField()
    lng = models.FloatField()
    
    def __unicode__(self):
        return u'[name: %s, url: %s, lat: %s, lng: %s]' % (self.name, self.url, self.lat, self.lng)


class FestDate(models.Model):
    """
    Model representing a day for a festival.
    """
    festival = models.ForeignKey(Festival)
    day = models.DateField()

    def __unicode__(self):
        return u'[festival: %s, day: %s]' % (self.festival, self.day)
    
    class Meta:
        unique_together = ('festival', 'day')


class Artist(models.Model):
    """
    Model representing an artist that is being tracked for a festival.
    """
    mbid = models.CharField(max_length=36, primary_key=True)
    songkickid = models.CharField(max_length=20, unique=True, null=True)
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
        for festDate in dates:
            # TODO: do this in a smarter way, processors maybe?
            if festDate in concerts:
                # TODO: make sure it's not this festival!
                self.statuses.append(DailyStatus.NO)
            else:
                self.statuses.append(DailyStatus.MAYBE)
        return self

    def getConcertsForArtist(self, **kwargs):
        """
        Returns a map of date->concert for the given artist between the given dates.

        Keyword Arguments:
        minDate -- minimum date to request (required)
        maxDate -- maximum date to request (required)
        """
        # Build the request
        artistPathTerm = ('mbid:' + self.mbid) if (self.mbid is not None) else (self.songkickid)
        requestUrl = 'http://api.songkick.com/api/3.0/artists/%s/calendar.json' % artistPathTerm
        requestParams = {
            'apikey': Constants.songKickApiKey,
            'min_date': kwargs.get('minDate'),
            'max_date': kwargs.get('maxDate')
        }

        # Retrieve and parse the response
        response = requests.get(requestUrl, params=requestParams)
        # print response.url
        json = response.json()['resultsPage']
        if json['status'] != 'ok':
            return None
        concerts = {}
        if json['totalEntries'] == 0:
            return concerts
        # Go over each event and add it to the concerts list
        for event in json['results']['event']:
            locObj = event['location']
            venueObj = event['venue']
            venueInfo = VenueInformation(locObj['lat'], locObj['lng'], locObj['city'], venueObj['displayName'])
            eventDate = parser.parse(event['start']['date']).date()
            eventInfo = EventInformation(eventDate, venueInfo)
            concerts[eventDate] = eventInfo
        return concerts

    def __unicode__(self): 
        return u'[mbid: %s, songkickid: %s, name: %s, festival: %s]' % \
               (self.mbid, self.songkickid, self.name, self.festival)


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


class VenueInformation():
    lat = None
    lng = None
    city = None
    venueName = None

    def __init__(self, lat, lng, city, venueName):
        self.lat = lat
        self.lng = lng
        self.city = city
        self.venueName = venueName

    def __unicode__(self):
        return u'[lat: %s, lng: %s, city: %s, venueName: %s]' % (self.lat, self.lng, self.city, self.venueName)
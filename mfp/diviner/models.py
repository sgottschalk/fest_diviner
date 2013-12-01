from django.db import models

#############################
# Database models
#############################
class Festival(models.Model):
    name = models.CharField(max_length = 100)
    url = models.CharField(max_length = 20, unique = True)
    
    def __unicode__(self):
        return u'[name: %s, url: %s]' % (self.name, self.url)
    
class FestDate(models.Model):
    festival = models.ForeignKey(Festival)
    day = models.DateField()
    
    def __unicode__(self):
        return u'[festival: %s, day: %s]' % (self.festival, self.day)
    
    class Meta:
        unique_together = ('festival', 'day')

class Artist(models.Model):
    mbid = models.CharField(max_length = 36, primary_key = True)
    songkickid = models.CharField(max_length = 20, unique = True)
    name = models.CharField(max_length = 100)
    festival = models.ForeignKey(Festival)
    
    def __unicode__(self): 
        return u'[mbid: %s, songkickid: %s, name: %s, festival: %s]' % (self.mbid, self.songkickid, self.name, self.festival)

#############################
# Application models
#############################
class MusicBrainzArtist():
    mbid = None
    name = None
    
    def __init__(self, mbid, name):
        self.mbid= mbid
        self.name = name
        
    def __unicode__(self):
        return u'[mbid: %s, name: %s]' % (self.mbid, self.name)
        
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
        return u'[mbid: %s, songkickid: %s, name: %s, events: %s]' % (self.mbid, self.songkickid, self.name, self.events)

class EventInformation():
    date = None
    venueInformation = None
    
    def __init__(self, date, venueInformation):
        self.date = date
        self.venueInformation = venueInformation
    
    def __unicode__(self):
        return u'[date: %s, venueInformation: %s]' % (self.date, self.venueInformation)
    
class VenueInformation:
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
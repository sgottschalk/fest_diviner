from django.db import models

class Festival(models.Model):
    name = models.CharField(max_length = 100)
    url = models.CharField(max_length = 20, unique = True)
    
    def __unicode__(self):
        return u'name: %s, url: %s' % (self.name, self.url)
    
class FestDate(models.Model):
    festival = models.ForeignKey(Festival)
    day = models.DateField()
    
    def __unicode__(self):
        return u'festival: %s, day: %s' % (self.festival, self.day)
    
    class Meta:
        unique_together = ('festival', 'day')

class Artist(models.Model):
    mbid = models.CharField(max_length = 36, primary_key = True)
    name = models.CharField(max_length = 100)
    festival = models.ForeignKey(Festival)
    
    def __unicode__(self): 
        return u'mbid: %s, name: %s, festival: %s' % (self.mbid, self.name, self.festival)

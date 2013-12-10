from diviner.models import MusicBrainzArtist, Artist
import musicbrainzngs as mb

def initializeConnection():
    mb.set_useragent('musicfestivalplanning', '0.1')

def searchForArtistByName(name):
    initializeConnection()

    searchResults = mb.search_artists(artist=name)
    artists = []
    for artist in searchResults['artist-list']:
        artists.append(MusicBrainzArtist(artist['id'], artist['name']))
    return artists

# Maybe use in the future, not sure if it returns not yet released albums or not.
def getReleasesByArtist(mbid):
    initializeConnection()

    results = mb.browse_release_groups(artist=mbid, release_type='album')
    for result in results['release-group-list']:
        print result

# messing around
# artist = Artist.objects.first()
# for result in searchForArtistByName('haim'):
#     print unicode(result)
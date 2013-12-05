from diviner.models import MusicBrainzArtist
import musicbrainzngs as mb

def searchForArtistByName(name):
    mb.set_useragent('musicfestivalplanning', '0.1')
    
    searchResults = mb.search_artists(artist=name)
    artists = []
    for artist in searchResults['artist-list']:
        artists.append(MusicBrainzArtist(artist['id'], artist['name']))
    return artists

# messing around
# for result in searchForArtistByName('arcade fire'):
#     print unicode(result)
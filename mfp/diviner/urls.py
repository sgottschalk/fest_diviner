from django.conf.urls import patterns, url
from diviner.views import SearchArtistView, FestivalView, AddArtistView

urlpatterns = patterns('',
    url(r'^festivals/(?P<festival_url>[^/]+)/add[/]?$', AddArtistView.as_view(), name="add_artist"),
    url(r'^festivals/(?P<festival_url>[^/]+)[/]?$', FestivalView.as_view(), name="festival_index"),
    url(r'^festivals/artists/search[/]?$', SearchArtistView.as_view(), name="search_artist"),
)
from django.conf.urls import patterns, include, url
from django.contrib import admin

from diviner.views import FestivalView, SearchArtistView, AddArtistView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^planner/', include('diviner.urls')),
    # url(r'^festivals/(?P<festival_url>[^/]+)/add[/]?$', AddArtistView.as_view(), name="add_artist"),
    # url(r'^festivals/(?P<festival_url>[^/]+)[/]?$', FestivalView.as_view(), name="festival_index"),
    # url(r'^festivals/artists/search[/]?$', SearchArtistView.as_view(), name="search_artist"),
)

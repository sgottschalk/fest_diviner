from django.conf.urls import patterns, include, url
from django.contrib import admin

from diviner.views import FestivalView


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^festivals/(?P<festival_url>[^/]+)[/]?$', FestivalView.as_view()),
)

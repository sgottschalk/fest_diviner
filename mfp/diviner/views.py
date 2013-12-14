import json
from django.http import HttpResponse
from django.views.generic.base import TemplateView, View

from diviner.models import Festival, ArtistSearch


# Create your views here.
class FestivalView(TemplateView):
    template_name = 'festival.html'
    
    def get_context_data(self, festival_url, **kwargs):
        context = super(FestivalView, self).get_context_data(**kwargs)
        festival = Festival.objects.get(url=festival_url)
        context['festival'] = festival
        context['dates'] = festival.festdate_set.all()
        context['artists'] = festival.artist_set.all()
        # Retrieve the info
        for artist in context['artists']:
            artist.adornStatusPerDay()
        return context


class SearchArtistView(View):
    def get(self, request, *args, **kwargs):
        searchTerm = request.GET.get("term", "")
        artistSearch = ArtistSearch(searchTerm)
        searchResults = artistSearch.executeSearch()
        returnJson = json.dumps([{'label': r.displayName, 'value': r.songkickId} for r in searchResults])
        return HttpResponse(returnJson, content_type="application/json")


class AddArtistView(View):
    def post(self, request, *args, **kwargs):
        # TODO: add it!
        print request.POST.get("songkickId")
        return HttpResponse('hi')
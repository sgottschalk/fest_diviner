from django.views.generic.base import TemplateView

from diviner.models import Festival, FestDate, Artist


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
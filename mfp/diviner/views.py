from django.views.generic.base import TemplateView

from diviner.models import Festival, FestDate, Artist


# Create your views here.
class FestivalView(TemplateView):
    template_name = 'festival.html'
    
    def get_context_data(self, festival_url, **kwargs):
        context = super(FestivalView, self).get_context_data(**kwargs)
        festival = Festival.objects.get(url = festival_url)
        context['festival'] = festival
        context['dates'] = FestDate.objects.filter(festival = festival)
        artists = Artist.objects.filter(festival = festival)
        context['artists'] = artists
        return context
from django.views.generic.base import TemplateView

from diviner.models import Festival


# Create your views here.
class FestivalView(TemplateView):
    template_name = 'festival.html'
    
    def get_context_data(self, festival_url, **kwargs):
        context = super(FestivalView, self).get_context_data(**kwargs)
        context['festival'] = Festival.objects.get(url = festival_url)
        return context
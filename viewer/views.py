from django.http import HttpResponse
from django.views.generic import TemplateView

from viewer.models import Event


def main(request):
  s = request.GET.get('s', '')
  return HttpResponse(f'Hello, {s} world!')

class EventsView(TemplateView):
  template_name = 'main_page.html'
  extra_context = {'events': Event.objects.all()}
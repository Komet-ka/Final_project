from django.http import HttpResponse

def main(request):
  s = request.GET.get('s', '')
  return HttpResponse(f'Hello, {s} world!')
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    template = 'index_small_chart.html'
    return render(request, template)
    #return HttpResponse('Main text')

# any output on page
def marketdata(request):
    return HttpResponse('Any text')

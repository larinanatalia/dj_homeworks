import csv

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings

def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    current_page = int(request.GET.get('page',1))
    content = []
    with open( settings.BUS_STATION_CSV, newline='') as f:
        reader = csv.DictReader(f)
        for i in reader:
            content.append({'Name': i['Name'], 'Street': i['Street'], 'District': i['District']})

    paginator = Paginator(content, settings.ITEMS_PER_PAGE)
    page_obj = paginator.get_page(current_page)
    if page_obj.has_next():
        next_page_url = reverse('bus_stations') + f'?page={page_obj.next_page_number()}'
    else:
        next_page_url = None
    if page_obj.has_previous():
        prev_page_url = reverse('bus_stations') + f'?page={page_obj.previous_page_number()}'
    else:
        prev_page_url = None

    return render(request, 'index.html', context={
        'bus_stations': page_obj,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })


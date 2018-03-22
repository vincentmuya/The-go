from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Location
import datetime as dt
from django.db import transaction
import googlemaps
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers

gmaps = googlemaps.Client(key='AIzaSyC14hiJhxMKNF4T4JCkDWyITjz8CoU2aco')
geo_result = gmaps.geocode('nairobi')
print(geo_result)
# Create your views here.
def index(request):
    test = "Code running"
    if 'address' in request.GET and request.GET['address']:
        address = request.GET.get("address")
        geo_result = gmaps.geocode('adams')
        print(geo_result)
        latitude = geo_result[0]['geometry']['location'].get('lat')
        longitude = geo_result[0]['geometry']['location'].get('lng')
        location = Location()
        location.name = address
        location.latitude = latitude
        location.longitude = longitude
        location.time = dt.datetime.now()
        location.save()

        return render(request, "index.html", {"latitude":latitude,"longitude":longitude})
    else:
        return render(request, 'index.html', {"test":test})

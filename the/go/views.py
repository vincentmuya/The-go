from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Location,Profile
import datetime as dt
from django.db import transaction
import googlemaps
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
import requests
from .forms import UserForm,ProfileForm

gmaps = googlemaps.Client(key='AIzaSyC14hiJhxMKNF4T4JCkDWyITjz8CoU2aco')
geo_result = gmaps.geocode('address')
print(geo_result)
# Create your views here.
@login_required(login_url='/accounts/login')
def index(request):
    test = "Code running"
    if 'address' in request.GET and request.GET['address']:
        address = request.GET.get('address')
        geo_result = gmaps.geocode('address')
        print(geo_result)
        latitude = geo_result[0]['geometry']['location'].get('lat')
        longitude = geo_result[0]['geometry']['location'].get('lng')
        location = Location()
        location.name = address
        location.latitude = latitude
        location.longitude = longitude
        location.time = dt.datetime.now()
        location.save()

        return render(request, "index.html", {"latitude":latitude,"longitude":longitude, "address":address})
    else:
        return render(request, 'index.html', {"test":test})

@login_required
@transaction.atomic
def update_profile(request, user_id):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/')

    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required(login_url='/accounts/login')
def profile(request, user_id):
    profile = Profile.objects.filter(user_id=request.user.id)
    print(profile)

    return render(request, "profile.html", {"profile": profile})

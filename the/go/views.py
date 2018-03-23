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
import twitter

api = twitter.Api(consumer_key='7HJYEfgpTJHw6aFnsHhOyt2Qs',
                  consumer_secret='sCTTtebaIUgZGXZWMW75juxcPYNdxL40slsUEVq6QZkfSLg21d',
                  access_token_key='1233519607-Sp3B4Qcjwwa6p51uxWRZ0NtgFtiziGf9gBuuFfI',
                  access_token_secret='rNY0h6pkEVd3kVLd7yZmBYtAhADRqeZ2z4Xjhz7d3t6wY')

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
        tweets =[]

        return render(request, "index.html", {"latitude":latitude,"longitude":longitude, "address":address, "tweets":getTweets()})
    else:
        return render(request, 'index.html', {"test":test})

'''internal function not called from the url '''
def getTweets():
    tweets =[]
    try:
        import twitter
        api = twitter.Api()
        latest = api.GetUserTimeLine('Ma3Route')
        for tweet in latest:
            status = tweet.text
            tweet_date = tweet.relative_created_at
            tweet.append({'status':status,'date': tweet_date})
    except:
        tweets.append({'status':'Follow @Ma3Route','date':'about 10 mins ago'})
    return{'tweets':tweets}

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

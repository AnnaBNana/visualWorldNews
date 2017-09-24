# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse,redirect
import os
import tweepy 
from django.http import JsonResponse
import urllib
import urllib2
from urlparse import urlparse
import json
import requests
import webhoseio
# Create your views here.
def index(request):
	
	return render(request, 'news/index.html')

def getTwitterData(request):
	# The consumer keys can be found on your application's Details
	# page located at https://dev.twitter.com/apps (under "OAuth settings")
	consumer_key="5C8RZIp057rzml2Oj3l8ATZtx"
	consumer_secret="FQo1SZ6UXPCrG6T4JAecSTI5eSIaBfxi42Eqa4wD1UzFKQY1vR"

	# The access tokens can be found on your applications's Details
	# page located at https://dev.twitter.com/apps (located
	# under "Your access token")
	access_token="153892256-w78HoYf8A7PGJggywriYeurDrITg81ADH0ssbIgy"
	access_token_secret="1HSr8fYacP6Eay9bWhmH9bFIPSkVxrZKdbie9MPop33Ne"

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
	trends = api.trends_available()

	for t in range(0,len(trends)):
	
		localeToCheck = trends[t].name
		
		# check to see if the local exists if id toes 
		locale_id = 0 # this will be whatever id it is
			
		else: 
			#insert in the locales via the api and update locale_id to be last insert id
			locale_id = 1 

	webHoseCount = getWebHoseData(localeToCheck)
	redditCount = get_reddit(localeToCheck)

	totalCount = webHoseCount + redditCount 

	#insert into entries via the api

	return JsonResponse('success':'true','response':trends)


def getWebHoseData(location):
	webhoseio.config(token="b99dbdf5-caac-4a2c-886a-fb8f37f365a0")

	query_params = {
	"q": "performance_score:>7 location:"+location,
	"ts": "1506110156153",
	"sort": "crawled" }

    
  	output = webhoseio.query("filterWebContent", query_params)
  	totalWebHose = len(output['posts'])
 	return totalWebHose
  	return JsonResponse({'success':'true','twitter_response':trends[2]})

def get_reddit(loc):
    reddit = praw.Reddit(client_id=REDDIT_ID,
                     client_secret=SECRET,
                     user_agent='web:visualWorldNews:v0.0.1 (by /u/anna_b_nana)')
    submissions = reddit.subreddit(loc).hot()
    count = 0
    for submission in submissions:
        count += 1
        print submission.title
     return count

def geoCodePlace(request):
	address = "1600 Amphitheatre Parkway, Mountain View, CA"
	api_key = "AIzaSyDNiwIGMuu9c6arwtK2Th11L2hm4mmXtGM"
	api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
	api_response_dict = api_response.json()

	if api_response_dict['status'] == 'OK':
	    latitude = api_response_dict['results'][0]['geometry']['location']['lat']
	    longitude = api_response_dict['results'][0]['geometry']['location']['lng']
	    print 'Latitude:', latitude
	    print 'Longitude:', longitud
	return JsonResponse({'success':'true','lat':latitude,'long':longitude})

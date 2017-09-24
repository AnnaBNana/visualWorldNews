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
import httplib
import praw
from django.utils.dateparse import parse_datetime
import datetime
import nexosisapi
import dateutil.parser as date_parser
import simplejson
from telesign.messaging import MessagingClient


SECRET = os.environ['REDDIT_SECRET']
REDDIT_ID = os.environ['REDDIT_ID']
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
	
	for t in range(1,len(trends)):
		try:
			localeToCheck = trends[t]['name']
			url = "https://parseapi.back4app.com/classes/locale"

			querystring = {"where":"{\"name\": {\"$regex\": \"^"+localeToCheck+"\"}}"}

			headers = {
			    'x-parse-application-id': "Ag24rU7mUcXfZhBZYnDa9Q2RbWPSF4hsZWBVCW61",
			    'x-parse-rest-api-key': "jbAkwQhfcchKlUL37pwbvVwYiTmLmJlV4QEgiLsP",
			    'cache-control': "no-cache",
			    'postman-token': "e3b38770-f50a-58af-5164-f85ac4d804b3"
			    }

			response = requests.request("GET", url, headers=headers, params=querystring)

			print(json.loads(response.text))

			jsonobject = json.loads(response.text)
			resultsLength =len(jsonobject['results'])

			


			if(resultsLength>0):
				print("***results")
				print(jsonobject['results'][0]['objectId'])
				print("*** end results")
				locale_id = jsonobject['results'][0]['objectId']
				latitude = jsonobject['results'][0]['latitude']
				longitude = jsonobject['results'][0]['longitude']
				#we have the location already
				# now we go and count and update

			else:
				# we geo code
				latLongObject = geoCodePlace(localeToCheck)
				latitude = str(latLongObject['lat'])
				longitude = str(latLongObject['long'])

				#add the location
				url = "https://parseapi.back4app.com/classes/locale"

				payload = "name="+localeToCheck+"&latitude="+latitude+"&longitude="+longitude+""
				headers = {
				   'content-type': "application/x-www-form-urlencoded",
				   'x-parse-application-id': "Ag24rU7mUcXfZhBZYnDa9Q2RbWPSF4hsZWBVCW61",
				   'x-parse-rest-api-key': "jbAkwQhfcchKlUL37pwbvVwYiTmLmJlV4QEgiLsP",
				   'cache-control': "no-cache",
				   'postman-token': "c9e12519-997e-8af6-5b24-40ed6a504431"
				   }

				response = requests.request("POST", url, data=payload, headers=headers)

				
				createdObject = json.loads(response.text)
				print("ADDED ***")
				print(createdObject)
				local_id = createdObject['objectId']
		except Exception as e:
			print(e)
			continue	
		
		try:
			webHoseCount = getWebHoseData(localeToCheck)
			redditCount = get_reddit(localeToCheck)
			thetotalCountForThisLocal = int(webHoseCount) + int(redditCount)
			print("**********TOTAL COUNT")
			print(thetotalCountForThisLocal)

			url2 = "https://parseapi.back4app.com/classes/entries"

			payload2 = "locale_id="+str(locale_id)+"&count="+str(thetotalCountForThisLocal)+"&lat="+latitude+"&long="+longitude+""
			headers2 = {
			   'content-type': "application/x-www-form-urlencoded",
			   'x-parse-application-id': "Ag24rU7mUcXfZhBZYnDa9Q2RbWPSF4hsZWBVCW61",
			   'x-parse-rest-api-key': "jbAkwQhfcchKlUL37pwbvVwYiTmLmJlV4QEgiLsP",
			   'cache-control': "no-cache",
			   'postman-token': "c9e12519-997e-8af6-5b24-40ed6a504431"
			   }

			entryResponse = requests.request("POST", url2, data=payload2, headers=headers2)

					
			createdEntry = json.loads(entryResponse.text)
			print("CREATED ENTRY RESPONSE ***")
			print(createdEntry)
			createdEntryObjectId = createdEntry['objectId']
		except Exception as c:
			print(c)

		#get all from table where object id 

		try:
			url3 = "https://parseapi.back4app.com/classes/entries"

			querystring3 = 'where={"locale_id":"'+locale_id+'"}'

			headers = {
			    'x-parse-application-id': "Ag24rU7mUcXfZhBZYnDa9Q2RbWPSF4hsZWBVCW61",
			    'x-parse-rest-api-key': "jbAkwQhfcchKlUL37pwbvVwYiTmLmJlV4QEgiLsP",
			    'cache-control': "no-cache",
			    'postman-token': "e3b38770-f50a-58af-5164-f85ac4d804b3"
			}

			existingEntries = requests.request("GET", url3, headers=headers, params=querystring3)

			print("***EXISTING ENTRIES***")
			print(json.loads(existingEntries.text))

			jsonExistingobject = json.loads(existingEntries.text)
			resultsLength =len(jsonExistingobject['results'])

			total =0
			for result in jsonExistingobject['results']:
				total += int(result['count'])

			average = total / resultsLength
			#update the average for that locale
			url4 = "https://parseapi.back4app.com/classes/entries/"+createdEntryObjectId+""

			payload = "average="+str(average)+""
			headers4 = {
		    'content-type': "application/x-www-form-urlencoded",
		    'x-parse-application-id': "Ag24rU7mUcXfZhBZYnDa9Q2RbWPSF4hsZWBVCW61",
		    'x-parse-rest-api-key': "jbAkwQhfcchKlUL37pwbvVwYiTmLmJlV4QEgiLsP",
		    'cache-control': "no-cache",
		    'postman-token': "03d1a4fd-1b79-43eb-7961-df6f483cac4b"
		    }

			updateAverageResponse = requests.request("PUT", url4, data=payload, headers=headers4)

			print("UPDATED AVERAGE***")
			print(average)
			print(updateAverageResponse.text)

			#go through each count, average and update
			print("CREATED ENTRY****")
			print(createdEntry)
		except Exception as d:
			print(d)

		# once we have created the entry now we go back and get an average
	#insert into entries via the api
	return JsonResponse({'success':'true','total_count':totalCount})


def getWebHoseData(location):
	webhoseio.config(token="b99dbdf5-caac-4a2c-886a-fb8f37f365a0")

	query_params = {
	"q": "performance_score:>7 location:"+location,
	"ts": "1506110156153",
	"sort": "crawled" }

    
  	output = webhoseio.query("filterWebContent", query_params)
  	totalWebHose = len(output['posts'])
 	return totalWebHose
  	# return JsonResponse({'success':'true','twitter_response':trends[2]})

def get_reddit(loc):
	reddit = praw.Reddit(client_id=REDDIT_ID, client_secret=SECRET, user_agent='web:visualWorldNews:v0.0.1 (by /u/anna_b_nana)')
	submissions = reddit.subreddit(loc).hot()
	count = 0
	try:
		for submission in submissions:
			count += 1
			print submission.title
		return count
	except Exception as e:
		print(e)
		

def geoCodePlace(location):
	address = location
	api_key = "AIzaSyDNiwIGMuu9c6arwtK2Th11L2hm4mmXtGM"
	api_response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={0}&key={1}'.format(address, api_key))
	api_response_dict = api_response.json()

	if api_response_dict['status'] == 'OK':
	    latitude = api_response_dict['results'][0]['geometry']['location']['lat']
	    longitude = api_response_dict['results'][0]['geometry']['location']['lng']
	    
	return {'lat':latitude,'long':longitude}

def forecast(request):
	url = "https://parseapi.back4app.com/classes/entries"

	headers = {
	    'x-parse-application-id': "Ag24rU7mUcXfZhBZYnDa9Q2RbWPSF4hsZWBVCW61",
	    'x-parse-rest-api-key': "jbAkwQhfcchKlUL37pwbvVwYiTmLmJlV4QEgiLsP",
	    'cache-control': "no-cache",
	    'postman-token': "a1a7a003-bc60-f717-43b4-43a1de03150a"
	    }

	response = requests.request("GET", url, headers=headers)

	# print(response.text)
	client = nexosisapi.Client('key2155ea7ca6af4e289a4e30f6d156dda4')
	jsonObject = json.loads(response.text)
	print(jsonObject)
	# client.datasets.create('news', jsonObject['results'])


	# datasets = client.datasets.list()
	# print(datasets)

	return JsonResponse({'success':'true','response':jsonObject['results']})


def frontEndData(request):
	print(datetime.datetime.now())
	now = datetime.datetime.now()
	nowString = str(now)
	fiveMinutesAgo = now - datetime.timedelta(minutes=60)
	print("***fiveminutesago")
	print(fiveMinutesAgo)

	url = "https://parseapi.back4app.com/classes/entries"

	querystring = 'where={"createdAt":{"$gt":{"__type":"Date","iso":"'+str(fiveMinutesAgo)+'"}}}'

	headers = {
			    'x-parse-application-id': "Ag24rU7mUcXfZhBZYnDa9Q2RbWPSF4hsZWBVCW61",
			    'x-parse-rest-api-key': "jbAkwQhfcchKlUL37pwbvVwYiTmLmJlV4QEgiLsP",
			    'cache-control': "no-cache",
			    'postman-token': "e3b38770-f50a-58af-5164-f85ac4d804b3"
	}
	existingEntries = requests.request("GET", url, headers=headers, params=querystring)
	# print(existingEntries)
	jsonObject = json.loads(existingEntries.text)
	# print(jsonObject['results'])
	print("****main results")

	mainResults = jsonObject['results']
	print(mainResults)
	newResults = []
	# print(len(mainResults))
	resultLength = len(mainResults)
	for x in range(1,len(mainResults)):
		# print("RESULT LOOP")

		# print("***EXISTING ENTRIES***")
		# print(json.loads(existingEntries.text))

		jsonExistingobject = json.loads(existingEntries.text)
		# print("***EXISTING OBJECT IN FRONT END DATA FUNCTION")
		# print(jsonExistingobject['results'][0]['average'])
		# print("RESULT RESULT")
	
		# print("END RESULT")
		try:
			newResults.append([mainResults[x]['long'],mainResults[x]['lat'],mainResults[x]['average'],mainResults[x]['count']])
		except Exception as e:
			print(e)
		# look up that locale id and average
		# insert the average into that object

	return JsonResponse({'success':'true','response':newResults})
	#select all from entries where count is greater than 75 for the latest date
	#loop through object
	#if the location average

def textAlert(request):
	confirmation = {"message": "Success"}
	print request.POST['phone_number']
	customer_id = "A2BBC2E2-9E5E-42AC-AA47-83F3F71E32B0"
	# api_key = os.environ['TELESIGN_KEY']
	api_key = "bgjWBxe+1UYKxjED0/Bk1m71u2tLwGrKJOu5+N+ZnvRuw+dsvjTy7PkjXjQlIcKIpAB7j1gRW8a1C5YRFhwXpw=="

	print(customer_id, api_key)

	phone_number = request.POST['phone_number']
	message = "You are signed up for alerts about " + request.POST['location']
	message_type = "ARN"

	messaging_client = MessagingClient(customer_id, api_key)
	response = messaging_client.message(phone_number, message, message_type)

	print(response.json)
	return JsonResponse(confirmation)
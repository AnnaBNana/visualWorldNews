from __future__ import print_function
import os
import requests
import praw
from telesign.messaging import MessagingClient

# SECRET = os.environ['REDDIT_SECRET']
# REDDIT_ID = os.environ['REDDIT_ID']

# def get_reddit(loc):
#     reddit = praw.Reddit(client_id=REDDIT_ID,
#                      client_secret=SECRET,
#                      user_agent='web:visualWorldNews:v0.0.1 (by /u/anna_b_nana)')
#     submissions = reddit.subreddit(loc).hot()
#     count = 0
#     for submission in submissions:
#         count += 1
#         print submission.title
#     print submissions.yielded

# get_reddit('Ottawa')

# customer_id = os.environ['TELESIGN_ID']
customer_id = "A2BBC2E2-9E5E-42AC-AA47-83F3F71E32B0"
# api_key = os.environ['TELESIGN_KEY']
api_key = "bgjWBxe+1UYKxjED0/Bk1m71u2tLwGrKJOu5+N+ZnvRuw+dsvjTy7PkjXjQlIcKIpAB7j1gRW8a1C5YRFhwXpw=="

print(customer_id, api_key)

phone_number = "15107543279"
message = "You're scheduled for a dentist appointment at 2:30PM."
message_type = "ARN"

messaging_client = MessagingClient(customer_id, api_key)
response = messaging_client.message(phone_number, message, message_type)

print(response.json)
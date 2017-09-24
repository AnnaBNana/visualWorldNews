import os
import requests
import praw

SECRET = os.environ['REDDIT_SECRET']
REDDIT_ID = os.environ['REDDIT_ID']

def get_reddit(loc):
    reddit = praw.Reddit(client_id=REDDIT_ID,
                     client_secret=SECRET,
                     user_agent='web:visualWorldNews:v0.0.1 (by /u/anna_b_nana)')
    submissions = reddit.subreddit(loc).hot()
    count = 0
    for submission in submissions:
        count += 1
        print submission.title
    print submissions.yielded

get_reddit('Ottawa')


import configparser

import datetime

import pandas as pd

import pathlib

import praw

import sys

# Full path to current directory
script_path = pathlib.Path(__file__).parent.resolve()

# Parse the configuration file
parser = configparser.ConfigParser()
parser.read(f"{script_path}/pipeline.conf")

# Store our configuration variables
SECRET = parser.get("reddit_config", "secret")
DEVELOPER = parser.get("reddit_config", "developer")
NAME = parser.get("reddit_config", "name")
CLIENT_ID = parser.get("reddit_config", "client_id")

# Name of our output file
date = sys.argv[1]
date = date[:10]
output_name = date

# Create a PRAW instance
reddit_read_only = praw.Reddit(client_id=CLIENT_ID,        
                               client_secret=SECRET,
                               user_agent="My User Agent")

# Specify subreddit we're interested in
subreddit = reddit_read_only.subreddit("dataengineering")

# Take top 30 posts of the past month
posts = subreddit.top('month', limit = 30)

# Dictionary to store data
posts_dict = {"ID" : [],
              "Title" : [],
              "Text" : [],
              "Score" : [],
              "Comments" : [],
              "URL" : [],
              "Comment" : [],
              "DateExecuted" : [],
              "DatePosted" : []}

# For each post, collect data and store in dictionary
for x, post in enumerate(posts):

    url = "https://www.reddit.com" + post.permalink

    posts_dict["ID"].append(post.id)
    posts_dict["Title"].append(post.title)
    posts_dict["Text"].append(post.selftext)
    posts_dict["Score"].append(post.score)
    posts_dict["Comments"].append(post.num_comments)
    posts_dict["URL"].append(url)
    posts_dict["DateExecuted"].append(date)
    posts_dict["DatePosted"].append(datetime.datetime.fromtimestamp(post.created))
  
    try:
      posts_dict['Comment'].append(post.comments[0].body)
    except:
      posts_dict['Comment'].append('Unknown')

# Store data to dataframe and save it to CSV file
top_posts_week = pd.DataFrame(posts_dict)
top_posts_week = top_posts_week.replace(',','', regex=True)
top_posts_week.to_csv(f"{script_path}/{output_name}.csv", index = False)

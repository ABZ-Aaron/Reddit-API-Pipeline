import praw
import json
import pandas as pd
import datetime

# Name output file
now = datetime.datetime.now()
day = now.day
month = now.month
year = now .year
week_num = datetime.date(year, day, month).isocalendar()[1]
output_name = f"{year}-{month}-{day}_WK{week_num}"

## Path of application
path = "/Users/aaronwright/Documents/Tech/Projects/RedditApp"

# Load in configuration data from our JSON file
with open(f'{path}/extraction/secrets/secret_reddit.json', 'r') as f:
  config_data = json.load(f)

# Save our JSON data
DEVELOPER = config_data['DEVELOPER']
SECRET = config_data['SECRET']
NAME = config_data['NAME']
CLIENT_ID = config_data['CLIENT_ID']

# Create a PRAW instance
reddit_read_only = praw.Reddit(client_id=CLIENT_ID,        
                               client_secret=SECRET,
                               user_agent="My User Agent")

# Specify subreddit we're interested in
subreddit = reddit_read_only.subreddit("dataengineering")

# Take top 10 posts of the past week
posts = subreddit.top('week', limit = 10)

# Dictionary to store data
posts_dict = {"Title" : [],
              "Text" : [],
              "ID" : [],
              "Score" : [],
              "Comments" : [],
              "URL" : [],
              "Comment" : [],
              "Date" : []}

# For each post, collect data and store in dictionary
for x, post in enumerate(posts):

    url = "https://www.reddit.com" + post.permalink

    posts_dict["ID"].append(post.id)
    posts_dict["Title"].append(post.title)
    posts_dict["Text"].append(post.selftext)
    posts_dict["Score"].append(post.score)
    posts_dict["Comments"].append(post.num_comments)
    posts_dict["URL"].append(url)
    posts_dict["Date"].append(output_name)
  
    try:
      posts_dict['Comment'].append(post.comments[0].body)
    except:
      posts_dict['Comment'].append('Unknown')

# Store data to dataframe and save it to CSV file
top_posts_week = pd.DataFrame(posts_dict)
top_posts_week.to_csv(f"{path}/extraction/output/{output_name}.csv", index=True)

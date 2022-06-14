# Overview

This pipeline was designed not only to create a nice looking dashboard, but also to develop skills in a range of tools. In fact, the tools used here (e.g., airflow, docker, redshift) are all very much overkill!

Regardless, if you decide to follow through the steps and set this up yourself, consider it good practice.

## How this pipeline works

Essentially there is one DAG (pipeline) running which extracts Reddit data from its API using Python's PRAW module. It is setup to extract data from the last 24 hours (assuming the subreddit isn't overly large and has a lot of posts) and stores this in a CSV, with fields such as post ID, author name, score of post, and so forth.

This CSV file is then loaded directly into an AWS S3 bucket (cloud storage), before being copied to AWS Redshift (cloud data warehouse).

This entire process is running with Apache Airflow (orchestration tool) which itself is running within a number of Docker containers. This saves us having to manually setup Airflow. 

Another two components make up this project that are not controlled with Airflow. 

First, we use dbt to connect to our data warehouse and transform the data. We don't really need to transform our data. We're only really using dbt to gain some familiarity with it and build our skills. 

Second, we will connect a BI tool to our warehouse (I recommend Google Data Studio, but feel free to use whatever you want) and create some cool looking visualisations.

Once all this is complete, you'll want to terminate your resources so as not to incur a charge. There are some options for keeping your dashboard active so that it can be shared with employers etc even once you terminate your resources. I'll cover this later.

If this sounds good to you, proceed to the next step.

---

[Next Step](reddit.md)

or

[Back to main README](../README.md)
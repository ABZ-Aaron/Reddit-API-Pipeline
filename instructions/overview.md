# Overview

This pipeline was designed not only to create a dashboard, but to gain exposure to a range of tools, develop new skills, and hopefully provide help to others.
## How this pipeline works

There is one DAG (pipeline) running which extracts Reddit data from its API using Python's [PRAW](https://praw.readthedocs.io/en/stable/) API wrapper. 

It is setup to extract data from the past 24 hours and store in a CSV with fields such as post ID, author name, and so forth.

This CSV is then loaded directly into an AWS S3 bucket (cloud storage) before being copied to AWS Redshift (cloud data warehouse).

This entire process is running with Apache Airflow (orchestration tool) running with Docker. This saves us having to manually setup Airflow. 

Another two components make up this project that are not controlled with Airflow. 

* First, we use dbt to connect to our data warehouse and transform the data. We're only using dbt to gain some familiarity with it and build our skills.

* Second, we will connect a BI tool to our warehouse and create some visualisations. I recommend Google Data Studio, but feel free to use something else.

Proceed to the next step to get started.

---

[Next Step](reddit.md)

or

[Back to main README](../README.md)

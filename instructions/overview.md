# Overview

This pipeline was designed not only to create a dashboard, but to gain exposure to a range of tools, develop new skills, and hopefully provide help to others.

## How this pipeline works

The pipeline is a single DAG which extracts Reddit data using the Reddit API. Python's [PRAW](https://praw.readthedocs.io/en/stable/) API wrapper is used here. 

It is setup to extract data from the past 24 hours and store in a CSV with fields such as post ID, author name, among others.

This CSV is then loaded directly into an AWS S3 bucket (cloud storage) before being copied to AWS Redshift (cloud data warehouse).

This entire process is running with Apache Airflow (orchestration tool) running with Docker (a container). This saves us having to manually setup Airflow. 

Another two components make up this project that are not controlled with Airflow:

* We use dbt to connect to our data warehouse and transform the data. We're only using dbt to gain some familiarity with it and build our skills.

* We connect a BI tool to our warehouse and create some visualisations. I recommend Google Data Studio, but feel free to use something else.

Proceed to the next step to get started.

---

[Next Step](reddit.md)

or

[Back to main README](../README.md)

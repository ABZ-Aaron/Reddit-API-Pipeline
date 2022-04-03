# Reddit ETL Pipeline

A data pipeline to extract Reddit data from [r/dataengineering](https://www.reddit.com/r/dataengineering/). Output is a PowerBI dashboard, which provides an overview of topics, posts and comments for subreddit.

## Motivation

Project was partly based on an interest in the Data Engineering subreddit and the kinds of questions and answers present there. 

It also provided a good opportunity to develop skills and experience in a range of tools. As such, project is more complex than required, utilising dbt, airflow, docker and cloud based storage.

## Architecture

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/process.png" width=70% height=70%>

1. Extract data using [Reddit API](https://www.reddit.com/dev/api/)
1. Load into [AWS S3](https://aws.amazon.com/s3/)
1. Copy into [AWS Redshift](https://aws.amazon.com/redshift/)
1. Transform using [dbt](https://www.getdbt.com)
1. Create [PowerBI](https://powerbi.microsoft.com/en-gb/) Dashboard
1. Orchestrate with [Airflow](https://airflow.apache.org) installed via [Docker](https://www.docker.com)

## Output

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/dashboard2.png" width=100% height=100%>

## Setup

If you would like to setup this pipeline, follow the below steps. Feel free to make improvements/changes. 

1. Clone Repo

    ```bash
    cd ~
    git clone https://github.com/ABZ-Aaron/Reddit-API-Pipeline.git
    cd Reddit-API-Pipeline
    ```
1. Reddit API Configuration ~ [see here](instructions/reddit.md)
1. Setup AWS Account ~ [see here](instructions/aws.md)
1. Setup AWS Redshift ~ [see here](instructions/setup_redshift.md)
1. Update Configuration Details ~ [see here](instructions/config.md)
1. Setup Docker & Airflow ~ [see here](instructions/docker_airflow.md)
1. Setup dbt ~ [see here](instructions/dbt.md)
1. Create Dashboard ~ [see here](instructions/powerbi.md)
1. Terminate Resources ~ [see here](instructions/.md)

## Improvements

There's a number of improvements that can be made here, which I'll implement at a later point!

* Use [Pushshift.io](https://www.reddit.com/r/pushshift/comments/bcxguf/new_to_pushshift_read_this_faq/) API instead of [PRAW](https://praw.readthedocs.io/en/stable/).

  One major issue with this project is that the Airflow DAG and extract script was initially designed to pull Reddit data based on the execution date. For example, if execution date is 20/05/2021, the DAG would only pull data that was posted on that date. Turns out this is not possible with PRAW, which reveals a design flaw in our pipeline. In its current state, we could end up with a file titled `25-12-2020.csv`, yet actual data in the file would be from a date later than this. This could be resolved using something like Pushshift, which allows us to specify date ranges.

* Improve Dashboard Output

  Only a very basic dashboard was generated. However something more interesting could be developed given more time.

* Testing

  No form of testing was implemented for this project, other than what we wrote for dbt. Unit and Integration tests could be implemented throughout the process to ensure data quality.

* Simplify Process

  The use of Airflow and dbt is overkill. Alternative ways to run this pipeline could be with Cron for orchestration and PostgreSQL for storage. We could also utilise AWS Lambdas and Step functions.

* Stream over Batch Processing

  If we want our Dashboard to always be up-to-date, we could benefit from something like Kafka.








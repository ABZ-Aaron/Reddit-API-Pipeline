# Reddit ETL Pipeline

A data pipeline to extract Reddit data from [r/dataengineering](https://www.reddit.com/r/dataengineering/). 

Output is a PowerBI dashboard, which provides an overview of topics, posts and comments for subreddit.

## Motivation

Project was partly based on an interest in the Data Engineering subreddit and the kinds of Q&A found there. 

It also provided a good opportunity to develop skills and experience in a range of tools. As such, project is more complex than required, utilising dbt, airflow, docker and cloud based storage.

## Architecture

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/process.png" width=70% height=70%>

1. Extract data using [Reddit API](https://www.reddit.com/dev/api/)
1. Load into [AWS S3](https://aws.amazon.com/s3/)
1. Copy into [AWS Redshift](https://aws.amazon.com/redshift/)
1. Transform using [dbt](https://www.getdbt.com)
1. Create [PowerBI](https://powerbi.microsoft.com/en-gb/) Dashboard
1. Orchestrate with [Airflow](https://airflow.apache.org) installed via [Docker](https://www.docker.com)
1. Create AWS resources with [Terraform](https://www.terraform.io)

## Output

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/dashboard2.png" width=70% height=70%>

## Setup

If you would like to setup this pipeline, follow the below steps. Feel free to make improvements/changes. This shouldn't cost you anything unless amend the pipeline to extract large amounts of data, or keep infrastructure up for 2+ months.

1. Clone Repo into home directory

    ```bash
    git clone https://github.com/ABZ-Aaron/Reddit-API-Pipeline.git
    cd Reddit-API-Pipeline
    ```
1. Reddit API Configuration ~ [see here](instructions/reddit.md)
1. Setup AWS Account ~ [see here](instructions/aws.md)
1. Setup AWS Infrastructure ~ [see here](instructions/setup_infrastructure.md)
1. Update Configuration Details ~ [see here](instructions/config.md)
1. Setup Docker & Airflow ~ [see here](instructions/docker_airflow.md)
1. Setup dbt ~ [see here](instructions/dbt.md)
1. Create Dashboard ~ [see here](instructions/powerbi.md)
1. Final Notes ~ [see here](instructions/terminate.md)

## Improvements

There's a number of improvements that can be made here, which I'll implement at a later point!


* Improve Dashboard Output

  Only a very basic dashboard was generated. However something more interesting could be developed given more time.

* Testing

  No form of testing was implemented for this project, other than what we wrote for dbt. Unit and Integration tests could be implemented throughout the process to ensure data quality.

* Simplify Process

  The use of Airflow and dbt is overkill. Alternative ways to run this pipeline could be with Cron for orchestration and PostgreSQL for storage. We could also utilise AWS Lambdas and Step functions.

* Stream over Batch Processing

  If we want our Dashboard to always be up-to-date, we could benefit from something like Kafka.








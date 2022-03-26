# Reddit Pipeline

This is an independent project developed after completing the DataTalksClub [BootCamp](https://github.com/DataTalksClub/data-engineering-zoomcamp).

It is an ELT pipeline to extract Reddit data from [r/dataengineering](https://www.reddit.com/r/dataengineering/) using Reddit's API and load it into a Data Warehouse, before transforming for analysis.

Due to specifications required, project is more complex than required, with the main purpose being to further develop skills using a variety of tools. 

## Architecture

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/process.png" width=60% height=60%>

* Architecture of pipeline

### Process

1. Extract data using [Reddit API](https://www.reddit.com/dev/api/)
1. Load into [AWS S3](https://aws.amazon.com/s3/)
1. Copy into [AWS Redshift](https://aws.amazon.com/redshift/)
1. Transform using [DBT](https://www.getdbt.com)
1. Create [PowerBI](https://powerbi.microsoft.com/en-gb/) Dashboard
1. Orchestrate with [Airflow](https://airflow.apache.org) installed via [Docker](https://www.docker.com)

### Expected Output

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/dashboard1.png" width=60% height=60%>

* Dashboard in PowerBI

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/dashboard1.png" width=60% height=60%>

* Dashboard with Filter in PowerBI
## Introduction

If you would like to set this pipeline up yourself, follow the below steps.
## Clone Repo & Setup

First step is to clone the Reddit App repo which contains files and folder required for this pipeline. Clone this into your home directory:

```bash
git clone https://github.com/ABZ-Aaron/Reddit-API-Pipeline.git
```
* Clone git repo

## Reddit API

To extract Reddit data, we can use it's API (Application Programming Interface). To use this, you'll need to create an `app`. 

To do this, first setup a Reddit account if you don't have one, then navigate [here](https://www.reddit.com/prefs/apps) and create the app. Make sure you select `script` from the radio buttons during the setup process.

Once setup, take a note of the `name` you gave the app, the `App ID`, and the `API Secret Key`.

## Setup AWS

We'll be using the cloud to store and transform our Reddit data. In our case, well use Amazon Web Service (AWS) which offers a free tier.

1. Setup a personal [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start). Follow instructions [here](https://aws.amazon.com/getting-started/guides/setup-environment/module-one/) and setup with free tier.

2. Secure your account following these [steps](https://aws.amazon.com/getting-started/guides/setup-environment/module-two/). 

    Here we are setting up MFA for the root user. The root is a special account that has access to everything. Therefore it's important we secure this. We'll also setup IAM users which will have their own set of permissions, in this case, admin permissions.

3. Setup CLI following this [guide](https://aws.amazon.com/getting-started/guides/setup-environment/module-three/). 

    This allows us to control AWS services from the command line interface. We'll need to configure credentials for CLI to use.

## Setup Redshift

Redshift is a data warehousing solution offered by AWS. This will be the end destination for our data. We'll first need to setup a Redshift cluster.

To setup AWS Redshift, you can use AWS's infrastructure-as-code tool `CloudFormation` by running the following steps:

```bash
cd ~/Reddit-API-Pipeline/cloudformation
```
* Change into relevant directory

```bash
vim setup_redshift.yml
```
* Open the YML file. If vim doesn't work, open by any means you wish. Once open, update the password field with the password for the admin account setting up the cluster. Save and exit.

```bash
aws cloudformation deploy --template-file setup_redshift.yml --stack-name myredshiftstack --capabilities CAPABILITY_NAMED_IAM    
```
* Deploy redshift. This will also create an IAM Role which allows Redshift to read from S3.

If you wish to delete the resources created, run the following. Note you can also delete the resources using the cloudformation UI in AWS.

```bash
aws cloudformation delete-stack --stack-name myredshiftstack  
```

In the AWS Console, you can navigate to CloudFormation using the search bar, and check the status of your stack. If you navigate to Redshift using the search bar, you should also see your cluster setup.

## ijweoifjiowejf

Next, you'll need to create a configuration file in the correct folder where you'll store some AWS details:

```bash
cd ~/Reddit-API-Pipeline/airflow/extraction
```
* Change directory into extraction folder

```bash
touch pipeline.conf
```
* Create configuration file

## Running Docker with Airflow

To orchestrate our pipeline, we'll be using Apache Airflow, which allows us to define [DAGs](https://en.wikipedia.org/wiki/Directed_acyclic_graph). Installing it can be a bit tricky, so for this, we'll install it with Docker. 

Docker as something that allows us to create and maintain containers. These are a bit like a special kind of virtual machine which, in our case, includes everything we need to run Airflow.

### Installing Docker

1. First you'll need to install Docker. Follow the instructions [here](https://docs.docker.com/get-docker/), selecting the OS your are currently using, as installation instructions differ between each one.

1. Next, you'll want to install Docker Compose. Find the instructions [here](https://docs.docker.com/compose/install/.) for your OS.

### Running Airflow

To start our pipeline, we'll need to kick of Airflow. To do so, navigate to the airflow directory in the cloned repo:

```bash
cd ~/RedditApp/airflow
```
* Navigate to airflow directory, assuming the repo was copied to your home folder

```bash
docker-compose up airflow-init
```
• Initialise the airflow database

```bash
docker-compose up
```
* Run airflow

If you have any issues, check [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).



## Setting up DBT

Once our data has been loaded into our Data Warehouse, we'll want to transform it, making it ready for analysis.

1. Create a DBT account [here]()
1. Create a project or just stick to the default project created
1. Setup Up a Database Connection - Select Redshift
1. On the next page, enter the relevant Redshift details. This includes the `hostname`. You'll find this in the AWS Redshift console. It will start with the name of your cluster and end with `amazonaws.com`. It will also require the port (likely `5439`), the database name (likely `dev`). You'll also need the database username (likely `awsuser`) and password.
1. Once connection is established, choose `managed directory` and give it  a name on the following page. You can also choose Github if you have a Github repo setup for the DBT part of this project.
1. Once you've worked through these initial steps, click on `Start Developing`

You are now in an IDE which is connected to your Redshift cluster. Here we'll run some basic transformations on our data.

1. Click on `initialize project`. This will populate the directory on the left hand side with folder and files we may need.
2. Under the `models` folder, create new files called `text_posts.sql` and `schema.yml`. You can delete the `example` folder.
3. In the `schema.yml` file copy the following. Here we are defining some basic tests and documentation for our table.

```yaml
version: 2

models:
  - name: text_posts
    description: Reddit Data with Full Text column
    columns:
      - name: id
        description: Reddit ID of Post
        tests:
          - not_null
      - name: title
        description: Title of Reddit Post
      - name: text
        description: Body Text of Reddit Post
      - name: score
        description: Score of Reddit Post
      - name: comments
        description: Number of Comments for Post
      - name: url
        description: Full URL of Reddit Post
      - name: comment
        description: Top comment for Reddit Post
      - name: dateposted
        description: Date Reddit Data was Downloaded
      - name: dateexecuted
        description: Date Reddit Post was made
```
4. Under the `text_posts.sql` file, copy the following. This is very simply selecting all columns, but adding a new column which is a combination of columns (this is used as part of the final analysis). Feel free to transform the data in whichever way you want however.

```sql
SELECT id, 
       title, 
       text, 
       url,
       comment,
       comments,
       score,
       dateposted,
       dateexecuted,
       (title || ' ' || comment || ' ' || text) full_text
FROM dev.public.reddit
```

5. Under the `dbt_project.yml`, update it to the following. All we've really changed here is the project name to `reddit_project` and told DBT to create all models as tables.

```yaml
# Name your project! Project names should contain only lowercase characters
# and underscores. A good package name should reflect your organization's
# name or the intended use of these models
name: 'reddit_project'
version: '1.0.0'
config-version: 2

# This setting configures which "profile" dbt uses for this project.
profile: 'default'

# These configurations specify where dbt should look for different types of files.
# The `source-paths` config, for example, states that models in this project can be
# found in the "models/" directory. You probably won't need to change these!
model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"  # directory which will store compiled SQL files
clean-targets:         # directories to be removed by `dbt clean`
  - "target"
  - "dbt_packages"


# Configuring models
# Full documentation: https://docs.getdbt.com/docs/configuring-models

# In this example config, we tell dbt to build all models in the example/ directory
# as tables. These settings can be overridden in the individual model files
# using the `{{ config(...) }}` macro.
models:
  reddit_project:
    materialized: table
```

To test what we've done, we can run the following commands at the bottom of the DBT IDE and make sure an error isn't returned:

```bash
dbt run
```

```bash
dbt test
```

The next step is just to click `commit` to commit our changes.


If you ran `dbt run` above an no error was returned, a new table will have been created in our Redshift database, under a new schema name. 

To check this, navigate to your Redshift cluster in AWS, and click on Query Data on the top right (orange button). Here, you want to navigate to the `dev` database, select the relevant schema, and check that the new table is here. 

When you working in your DBT development environment, this is where the models are created.

We now want to setup a production run, as we wouldn't want analysts accessing our models from within our development area.

1. To do this, navigate to the left hand side menu and select `Environments` then click `New Environments`.

1. The `Type` option should be set to `Deployment`. Change the `Name` to something like `Production Run`.
1. Under `Deployment Credentials` enter your database username and password again. Also set a schema name, something like `Analytics` and Save.
1. Click on `New Job`
1. Give your job a name. Set environment as the `Production Run` you just created
1. Select the `Generate Docs` radio button
1. Under `Commands` ensure that `dbt run` and `dbt test` are both there.
1. Under `Triggers` ,normally you'd have this on a schedule, but for our purposes, just de-select so that it does not run on a schedule. We'll just run it manually. 
1. Once saved, run the job. You can then check the Redshift cluster, where you should find a new schema folder with our production table/model.

## Loading data into PowerBI

In progress...



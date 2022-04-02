<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/process.png" width=100% height=100%>

# Reddit ETL Pipeline

A data pipeline to extract Reddit data from [r/dataengineering](https://www.reddit.com/r/dataengineering/). Output is a PowerBI dashboard, which provides an overview of topics, posts and comments for subreddit.

Motivation for this project was partly based on an interest in the Data Engineering subreddit. It also provided a good opportunity to develop skills and experience in a range of tools. As such, project is more complex than required, utilising dbt, airflow, docker and cloud based storage.

## Table of Contents
1. [Architecture](#Architecture)
1. [Output](#ExpectedOutput)
1. [Introduction](#Introduction)
1. [Setup Reddit API](#SetupRedditAPI)
1. [Setup AWS](#SetupAWS)
1. [Setup Redshift](#SetupsRedshift)
1. [Configuration File](#ConfigFile)
1. [Docker & Airflow](#DockerAirflow)
1. [dbt](#DBT)
1. [Data Visualisation](#DataViz)
1. [The End](#FinalNotes)

---

## Architecture  <a name="Architecture"></a>

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/process.png" width=100% height=100%>

* Architecture of pipeline

1. Extract data using [Reddit API](https://www.reddit.com/dev/api/)
1. Load into [AWS S3](https://aws.amazon.com/s3/)
1. Copy into [AWS Redshift](https://aws.amazon.com/redshift/)
1. Transform using [DBT](https://www.getdbt.com)
1. Create [PowerBI](https://powerbi.microsoft.com/en-gb/) Dashboard
1. Orchestrate with [Airflow](https://airflow.apache.org) installed via [Docker](https://www.docker.com)

## Output <a name="ExpectedOutput"></a>

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/dashboard2.png" width=100% height=100%>

* Dashboard in PowerBI

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/dashboard1.png" width=100% height=100%>

* Dashboard with Filter in PowerBI

## Introduction <a name="Introduction"></a>

If you would like to set up a pipeline like this yourself, follow the below steps.
## Clone Repo & Setup <a name="CloneRepo&Setup"></a>

First step is to clone this repo, which contains files and folder required for this pipeline. Clone this into your home directory:

```bash
git clone https://github.com/ABZ-Aaron/Reddit-API-Pipeline.git
```
* Clone git repo

## Reddit API <a name="SetupRedditAPI"></a>

To extract Reddit data, we can use its API (Application Programming Interface). There's a couple steps you'll need to follow in order to set this up.

First create a Reddit account if you don't have one, then navigate [here](https://www.reddit.com/prefs/apps) and create an `app`, following the steps. Make sure you select `script` from the radio buttons during the setup process.

Once it's setup, take a note of the `name` you gave the app, the `App ID`, and the `API Secret Key`.

## Setup AWS <a name="SetupAWS"></a>

We'll be using the cloud to store our Reddit data. In our case, well use Amazon Web Service (AWS) which offers a free tier.

In our case, we'd be fine to just use a local database like Postgresql. However, consider this good practice.


1. Setup a personal [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start). Follow instructions [here](https://aws.amazon.com/getting-started/guides/setup-environment/module-one/) and setup with free tier.

2. Secure your account following these [steps](https://aws.amazon.com/getting-started/guides/setup-environment/module-two/). 

    Here we are setting up MFA for the root user. The root is a special account that has access to everything. Therefore it's important we secure this. We'll also setup IAM users which will have their own set of permissions, in this case, admin permissions.

3. Setup CLI following this [guide](https://aws.amazon.com/getting-started/guides/setup-environment/module-three/). 

    This allows us to control AWS services from the command line interface. 

One thing to always note when using AWS is the region (e.g. `us-east-1`). When accessing certain resources, you can change this on the top right of the AWS UI. If you find you're missing a redshift cluster (we'll set this up next) it may be because you're region isn't set to the one redshift was setup on. Change it to the correct region and you'll see your cluster.

## Setup Redshift <a name="SetupsRedshift"></a>

Redshift is a columnar data warehousing solution offered by AWS. This will be the end destination for our data. Let's setup a Redshift cluster.

We'll use AWS's infrastructure-as-code tool `CloudFormation`. This essentially allows us to setup AWS resources using code. If you've cloned this repo, you'll just need to run the following commands:

```bash
cd ~/Reddit-API-Pipeline/cloudformation
```
* Change into relevant directory

```bash
vim setup_redshift.yml
```
* Open the YML file. If vim doesn't work, open by any means you wish. 

Once file is open, update the password field with a unique password. Save and exit.

```bash
aws cloudformation deploy --template-file setup_redshift.yml --stack-name myredshiftstack --capabilities CAPABILITY_NAMED_IAM    
```
* Deploy redshift. This will also create an IAM Role which allows Redshift to read from S3.

If you wish to delete the resources created, run the following. Note you can also delete the resources using the cloudformation UI in AWS.

```bash
aws cloudformation delete-stack --stack-name myredshiftstack  
```

In the AWS Console, you can navigate to `CloudFormation` using the search bar, and check the status of your stack. 

If you navigate to Redshift using the search bar, you should also see that your cluster is now setup.

## Configuration File <a name="ConfigFile"></a>

Next, you'll need to create a configuration file in the correct folder where you'll store some AWS details:


```bash
touch ~/Reddit-API-Pipeline/airflow/extraction/pipeline.conf
```
* Create configuration file

Copy the following into this file, replacing the `XXXXXXX` values:

```conf
[boto_config]
access_key = XXXXXXXXX
secret_key = XXXXXXXXX
bucket_name = XXXXXXXX
account_id = XXXXXXXX

[redshift_config]
database = dev
username = awsuser
password = XXXXXXXXX
host =  XXXXXXXX
port = 5439
iam_role = RedShiftLoadRole

[reddit_config]
secret = XXXXXXXXX
developer = XXXXXXXX
name = XXXXXXXXX
client_id = XXXXXXXXX
```
* For the Boto Config, you'll need the `access_key` and `secret_key` generated from the User Account you would have generated when you setup and configured AWS. The bucket name should be something unique (e.g. yourname-reddit-s3-bucket). The Account ID you'll find in AWS.

* For Redshift Config, you'll need to input your Redshift `host` name, along with the `password` for the database. The `host` name can be found in the Redshift AWS Console, and will start with the name of your cluster, and end with `amazonaws.com`. The remaining field can be left as the default assuming you set Redshift up using the `Cloudformation` script.

* For the Reddit Config, these are the details you took note of after setting up your Reddit App.

## Running Docker with Airflow <a name="DockerAirflow"></a>

To orchestrate our pipeline, we'll be using Apache Airflow, which allows us to define [DAGs](https://en.wikipedia.org/wiki/Directed_acyclic_graph). Installing it can be a bit tricky, so for this, we'll install it with Docker. 

Docker is something that allows us to create and maintain containers. These are a bit like a special kind of virtual machine which, in our case, includes everything we need to run Airflow.

### Installing Docker <a name="Docker"></a>

1. First you'll need to install Docker. Follow the instructions [here](https://docs.docker.com/get-docker/), selecting the OS your are currently using, as installation instructions differ between each one.

1. Next, you'll want to install Docker Compose. Find the instructions [here](https://docs.docker.com/compose/install/.) for your OS.

### Running Airflow <a name="Airflow"></a>

To start our pipeline, we'll need to kick off Airflow. To do so, navigate to the airflow directory in the cloned repo:

```bash
cd ~/RedditApp/airflow
```
* Navigate to airflow directory

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```
* Create `.env` file. See [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) for more details if interested

```bash
docker-compose up airflow-init
```
* Initialise the airflow database

```bash
docker-compose up
```
* Run airflow

If you have any issues, check [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).

After a few minutes, Airflow should be fully running. You should now be able to access the Airflow Web Interface:

`http://localhost:8080`

Password and username are both `airflow`.

Once in, you'll see something like this:

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/process.png" width=100% height=100%>

Switch the DAG on with the button to the left of `etl_reddit_pipeline`. You can then run the DAG with the start button on the right hand side.

## Setting up DBT <a name="DBT"></a>

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

## Data Visualisation <a name="DataViz"></a>

It's up to you what kind of dashboarding / data viz tool you use. In my case, I used [PowerBI](https://powerbi.microsoft.com/en-gb/). For this, you'll need to use Windows OS. If you're on Mac or Linux, you can consider a virtualisation software like [virtualbox](https://www.virtualbox.org) to set use Windows.

If that's not an option, other BI tools won't differ too much from PowerBI.

To connect Redshift to PowerBI:

1. Create an account with PowerBI. If you don't have a work or school email address, consider setting up an account with a [temporary email address](https://tempmail.net), as it won't accept Gmail and other services used for personal accounts. 

2. Open PowerBI and click `Get Data`
3. Search for `Redshift` in the search box and click `Connect`
4. Enter your Redshift server/host name, and the name of the database (e.g. dev) and click `OK`
5. Enter the username (e.g. awsuser) and password for the database, and then select the relevant table you'd like to load in. 
6. You can now feel free to create some graphs and visualisations. Here's an example:

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/dashboard2.png" width=100% height=100%>

## Good Job <a name="FinalNotes"></a>

You should now have a functional data pipeline.

You'll most likely want to shut down the services you setup here so you don't incur a charge. 

1. Terminate your Redshift Cluster by running the following cloudformation command. Once complete, you can navigate to the Redshift console in AWS and double check you no longer have a cluster running (make sure you have selected the relevant region/location from the top right hand menu in AWS)

```bash
aws cloudformation delete-stack --stack-name myredshiftstack  
```

2. Manually delete the S3 Bucket and contents. You can do this via the AWS UI in the S3 Console.

3. Delete your DBT account if necessary


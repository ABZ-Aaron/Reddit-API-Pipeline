# Docker & Airflow

We're going to run our pipeline daily, for demonstration purposes, although this could be changed at a later point. Each day, we'll extract the top 10 Reddit posts for `r/DataEngineering`.

## Airflow

To orchestrate this, we'll be using Apache Airflow, which allows us to define [DAGs](https://en.wikipedia.org/wiki/Directed_acyclic_graph). Although Airflow is overkill in our case, consider it good practice. It will allow us automate our extraction and loading within our pipeline.

## Docker

Another tool we'll use is Docker. This allows us to create and maintain 'containers'. Think of a container a bit like a special kind of virtual machine which, in our case, includes everything we need to run Airflow, bypassing the need to install a bunch of dependencies.

### Installing Docker <a name="Docker"></a>

1. First install Docker. Follow the instructions [here](https://docs.docker.com/get-docker/).

1. Next install Docker Compose. Find the instructions [here](https://docs.docker.com/compose/install/.).

### Running Airflow <a name="Airflow"></a>

To start our pipeline, we'll need to kick off Airflow which requires a couple of prerequisite steps.

1. Create `.env` file and initialise the airflow database. See [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) for more details if interested.

    ```bash
    cd ~/Reddit-API-Pipeline/airflow
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    docker-compose up airflow-init
    ```
1. If using Windows, make a small update to the `~/Reddit-API-Pipeline/airflow/docker-compose.yaml` file.

    ```yaml
    # Replace this...
    - $HOME/.aws/credentials:/home/airflow/.aws/credentials:ro

    # With this...
     - %UserProfile%\.aws\credentials:/home/airflow/.aws/credentials:ro
    ```

    * Here we are specifying a volume, so when we run our container, the folder where our AWS credentials are stored will be "synced" with a folder on our container. This will allow our Docker container to find the AWS credentials and successfully run our scripts

1. Create our Airflow containers.

    ```bash
    docker-compose up
    ```

1. Give this a few minutes or more. Airflow should then be fully running, and you'll be able to access the Airflow Web Interface via `http://localhost:8080`. Password and username are both `airflow`.

    Once in, you'll see something like this:

    <img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/airflow.png" width=70% height=70%>

1. Switch the DAG on with the button to the left of `etl_reddit_pipeline`. You can then run the DAG with the start button on the right hand side.

## Explanation

If you check in the `airflow/dags` folder, you'll find a file titled `elt_reddit_pipeline.py`. This is our DAG which you saw in Airflow's UI. 

It's a very simple DAG. All it's doing is running 4 tasks, one after the other. These tasks are using `BashOperator`, meaning that they are running a bash command. Three of these tasks are running a bash command to call external Python scripts (these Python scripts exist within our docker container through the use of volumes). Read below for more details:

1. `extract_reddit_data_task`

    This is extracting Reddit data. Specifically, it's taking the top posts of the day from `r/DataEngineering` and collecting a few different attributes, like the top comment of each post. It's then saving this to a CSV within a temp folder.

1. `upload_to_s3`

    This is uploading the newly created CSV to AWS S3 for storage within the bucket Terraform created.

1. `copy_to_redshift`

    This is creating a table in Redshift if it doesn't already exist. It's then using the `COPY` command to copy data from the newly uploaded CSV file in S3 to Redshift.

## Note

Anyone issues with Airflow & Docker, have a read through [this](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).

---

[Previous Step](config.md) | [Next Step](dbt.md)

or

[Back to main README](../README.md)

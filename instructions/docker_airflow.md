# Docker & Airflow

We're going to run our pipeline daily, for demonstration purposes, although this could be changed at a later point. Each day, we'll extract the top Reddit posts for `r/DataEngineering`. Because `LIMIT` is set to `None` in the Reddit extraction script, it should in theory return all posts from the past 24 hours.

If you want to learn more about Airflow & Docker, have a look [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).

## Airflow

To orchestrate this, we'll be using Apache Airflow, which allows us to define [DAGs](https://en.wikipedia.org/wiki/Directed_acyclic_graph). Although Airflow is overkill in our case, consider it good practice. It will allow us automate our extraction and loading within our pipeline.

Tutorial [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)

## Docker

Another tool we'll use is Docker. This allows us to create and maintain 'containers'. Think of a container a bit like a special kind of virtual machine which, in our case, includes everything we need to run Airflow, bypassing the need to install a bunch of dependencies.

Tutorial [here](https://www.youtube.com/watch?v=3c-iBn73dDE)
### Installing Docker <a name="Docker"></a>

1. First install Docker. Follow the instructions [here](https://docs.docker.com/get-docker/).

1. Next install Docker Compose. Find the instructions [here](https://docs.docker.com/compose/install/.).

### Running Airflow <a name="Airflow"></a>

To start our pipeline, we'll need to kick off Airflow which requires a couple of prerequisite steps.

1. If using Windows, make a small update to the `~/Reddit-API-Pipeline/airflow/docker-compose.yaml` file.

    ```yaml
    # Replace this...
    - $HOME/.aws/credentials:/home/airflow/.aws/credentials:ro

    # With this...
     - %UserProfile%\.aws\credentials:/home/airflow/.aws/credentials:ro
    ```
    
    * Here we are specifying a volume, so when we run our container, the local folder where our AWS credentials are stored will be "synced" with a folder in the created containers. This will allow our Docker containers to find the AWS credentials and successfully run our scripts.

1. Increase CPU and Memory in Docker Desktop resource settings to whatever you think your PC can handle.

1. Run the following. You may be able to skip this step if you're not on linux. See [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html) for more details.

    ```bash
    cd ~/Reddit-API-Pipeline/airflow
    
    # Create folders required by airflow. 
    # dags folder has already been created, and 
    # contains the dag script utilised by Airflow
    mkdir -p ./logs ./plugins

    # This Airflow quick-start needs to know your
    # host user id
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```

1. Initialise the airflow database. This will take a few minutes. Make sure the Docker daemon (background process) is running before doing this.

    ```bash
    docker-compose up airflow-init
    ```

1. Create our Airflow containers. This could take a while. You'll know when it's done when you get an Airflow login screen at http://localhost:8080.

    ```bash
    docker-compose up
    ```

1. If interested, once containers are created, you can view them in Docker Desktop, or list them from the command line with:

    ```bash
    docker ps
    ```
1. You can even connect into a docker container and navigate around the filesystem if interested:

    ```bash
    docker exec -it <CONTAINER ID> bash
    ```

1. As mentioned above, navigate to `http://localhost:8080` to access the Airflow Web Interface. This is running within one of the Docker containers, which is mapping onto our local machine. If nothing shows up, give it a few minutes more. Password and username are both `airflow`.

    Once in, you'll see something like this:

    <img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/airflow.png" width=70% height=70%>

1. The dag `etl_reddit_pipeline` should be set to start running automatically (it may have already finished by the time you login). The next DAG run will run at midnight. If you click on the DAG and look under the Tree view, all the boxes should be dark green if the DAG run was successful. If there's any issues, this [resource](https://www.astronomer.io/guides/airflow-ui/) might help.

1. If you want to shut down the airflow containers run the following command from the airflow directory:

    ```bash
    docker-compose down
    ```

1. Or if you want stop and delete containers, delete volumes with database data and download images, run the following. This can be useful if you want to start from scratch:

    ```bash
    docker-compose down --volumes --rmi all
    ```

## Explanation

If you check in the `airflow/dags` folder, you'll find a file titled `elt_reddit_pipeline.py`. This is our DAG which you saw in Airflow's UI. 

In the `docker-compose.yaml` file, we've defined some volumes which I mentioned further up. You'll see that one of the lines is syncing the `dags` folder we have locally with the Docker container when the container is created via `docker-compose up`.

It's a very simple DAG. All it's doing is running 3 tasks, one after the other. This DAG will run everyday at midnight. It will also run once as soon as you create the Docker containers. These tasks are using `BashOperator`, meaning that they are running a bash command. The tasks here are running a bash command to call external Python scripts (these Python scripts also exist within our docker container through the use of volumes). You'll find them under the `extraction` folder. 

Read below for more details:

1. `extract_reddit_data_task`

    This is extracting Reddit data. Specifically, it's taking the top posts of the day from `r/DataEngineering` and collecting a few different attributes, like the number of comments. It's then saving this to a CSV within the /tmp folder.

1. `upload_to_s3`

    This is uploading the newly created CSV to AWS S3 for storage within the bucket Terraform created.

1. `copy_to_redshift`

    This is creating a table in Redshift if it doesn't already exist. It's then using the COPY command to copy data from the newly uploaded CSV file in S3 to Redshift. This is designed to avoid duplicate data based on post id. If the same post id is in a later DAG run load, then warehouse will be updated with that record. Read [here](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html) for information on the COPY command. 

## Note

Any issues with Airflow & Docker, have a read through [this](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html).

---

[Previous Step](config.md) | [Next Step](dbt.md)

or

[Back to main README](../README.md)

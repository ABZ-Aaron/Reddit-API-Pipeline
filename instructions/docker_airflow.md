# Docker & Airflow

We're going to run our pipeline daily, for demonstration purposes, although this could be changed at a later point. Each day, we'll extract the top Reddit posts for `r/DataEngineering`. Because `LIMIT` is set to `None` in the Reddit extraction script, it should in theory return all posts from the past 24 hours. Feel free to play around with this.

## Airflow

To orchestrate this, we'll use Apache Airflow, which allows us to define [DAGs](https://en.wikipedia.org/wiki/Directed_acyclic_graph). Although Airflow is overkill in our case, consider it good practice. It will allow us automate our extraction and loading within our pipeline.

Tutorial [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial.html)

## Docker

Another tool we'll use is Docker. This allows us to create and maintain 'containers'. Think of a container a bit like a special kind of virtual machine which, in our case, includes everything we need to run Airflow, bypassing the need to install a load of dependencies.

Tutorial [here](https://www.youtube.com/watch?v=3c-iBn73dDE)

## Airflow in Docker Info

For this project, the `docker-compose.yaml` file comes from the Airflow in Docker quick-start guide [here](https://airflow.apache.org/docs/apache-airflow/stable/start/docker.html). This defines all the services we need for Airflow, e.g., scheduler, web server, and so forth.

> **NOTE:** Ths quickstart shouldn't be used in production environments.

When we run this docker-compose file further down, it will start our containers/services. I've only changed a few things in this file:

* These two extra lines added under `volumes` will mount these folders on our local file system to the docker containers. You can see other volumes are defined, one being to mount the `./dags` folder (this is where we store dags airflow should run). The first line below mounts our `extraction` folder to `/opt/airflow`, which contains the scripts our airflow DAG will run. The second line mounts our aws credentials into the docker containers as read only.

    ```yaml
    - ./extraction:/opt/airflow/extraction
    - $HOME/.aws/credentials:/home/airflow/.aws/credentials:ro
    ```

* This line pip installs the specified packages within the containers. Note that there are others ways we could have done this.

    ```yaml
    _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:- praw boto3 configparser psycopg2-binary}
    ```

### Installing Docker <a name="Docker"></a>

1. First install Docker. Instructions [here](https://docs.docker.com/get-docker/).

1. Next install Docker Compose. Instructions [here](https://docs.docker.com/compose/install/.).

### Running Airflow <a name="Airflow"></a>

To start our pipeline, we need to kick off Airflow which requires a couple more prerequisite steps.

1. If using Windows, you may need to make a small update to the below line in the `docker-compose.yaml` file. Here we are mounting our aws credentials file on to a docker container.

    ```yaml
    - $HOME/.aws/credentials:/home/airflow/.aws/credentials:ro
    ```

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

1. Making sure you are still in the airflow directory, initialise the airflow database. This will take a few minutes. Make sure the Docker daemon (background process) is running before doing this. 

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
1. You can even connect into a docker container and navigate around the filesystem:

    ```bash
    docker exec -it <CONTAINER ID> bash
    ```

1. As mentioned above, navigate to `http://localhost:8080` to access the Airflow Web Interface. This is running within one of the Docker containers, which is mapping onto our local machine with port 8080. If nothing shows up, give it a few minutes more. Password and username are both `airflow`. For understanding the UI, I'd recommend looking at some guides like this [one](https://airflow.apache.org/docs/apache-airflow/stable/ui.html).


1. The dag `etl_reddit_pipeline` should be set to start running automatically once the containers are created. It may have already finished by the time you login. This option is set within the docker-compose file (`AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'false'`). The next DAG run will be at midnight. If you click on the DAG and look under the Tree view, all boxes should be dark green if the DAG run was successful. If there's any issues, this [resource](https://www.astronomer.io/guides/airflow-ui/) or the ones linked previously might help. Essentially, you'll want to click on any box that's red, click `logs` and scan through it until you find the issue.

1. If you want to shut down the airflow containers, run the following command from the airflow directory:

    ```bash
    docker-compose down
    ```

1. Or if you want stop and delete containers, delete volumes with database data and download images, run the following. This can be useful if you want to remove everything and start from scratch. It's a good idea to do some reading into docker commands before running something like this though, so you understand what it's doing.

    ```bash
    docker-compose down --volumes --rmi all
    ```

## Explanation

If you check in the `airflow/dags` folder, you'll find a file titled `elt_reddit_pipeline.py`. This is our DAG which you saw in Airflow's UI. 

It's a very simple DAG. All it's doing is running 3 tasks, one after the other. This DAG will run everyday at midnight. It will also run once as soon as you create the Docker containers. These tasks are using `BashOperator`, meaning that they are running a bash command. The tasks here are running a bash command to call external Python scripts (these Python scripts also exist within our docker container through the use of volumes). You'll find them under the `extraction` folder. 

Read below for more details:

1. `extract_reddit_data_task`

    This is extracting Reddit data. Specifically, it's taking the top posts of the day from `r/DataEngineering` and collecting a few different attributes, like the number of comments. It's then saving this to a CSV within the /tmp folder.

1. `upload_to_s3`

    This is uploading the newly created CSV to AWS S3 for storage within the bucket Terraform created.

1. `copy_to_redshift`

    This is creating a table in Redshift if it doesn't already exist. It's then using the COPY command to copy data from the newly uploaded CSV file in S3 to Redshift. This is designed to avoid duplicate data based on post id. If the same post id is in a later DAG run load, then warehouse will be updated with that record. Read [here](https://docs.aws.amazon.com/redshift/latest/dg/r_COPY.html) for information on the COPY command. 

---

[Previous Step](config.md) | [Next Step](dbt.md)

or

[Back to main README](../README.md)

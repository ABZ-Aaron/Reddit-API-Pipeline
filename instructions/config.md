
# Configuration

Next, you'll need to create a configuration file with your details. The extract and load scripts in our pipeline will utilise the details here.

## Setup

1. Create a configuration file under `~/Reddit-API-Pipeline/airflow/extraction/` called `configuration.conf`:

    ```bash
    touch ~/Reddit-API-Pipeline/airflow/extraction/configuration.conf
    ```

1. Copy in the following:

    ```conf
    [aws_config]
    bucket_name = XXXXX
    redshift_username = awsuser
    redshift_password = XXXXX
    redshift_hostname =  XXXXX
    redshift_role = RedShiftLoadRole
    redshift_port = 5439
    redshift_database = dev
    account_id = XXXXX
    aws_region = XXXXX

    [reddit_config]
    secret = XXXXX
    developer = XXXXX
    name = XXXXX
    client_id = XXXXX
    ```


1. Change `XXXXX` values

    * If you need a reminder of your `aws_config` details, change folder back into the terraform folder and run the command. It will output the values you need to store under `aws_config`. Just be sure to remove any `"` from the strings.

        ```bash
        terraform output
        ```
        
    * For `reddit_config` these are the details you took note of after setting up your Reddit App. Note the `developer` is your Reddit name.

---

[Previous Step](setup_infrastructure.md) | [Next Step](docker_airflow.md)

or

[Back to main README](../README.md)

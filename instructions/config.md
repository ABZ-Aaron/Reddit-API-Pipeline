
# Configuration

Next, you'll need to update the configuration file with your details. The extract and load scripts will utilise the details here.

## Setup

1. Create a configuration file under `~/Reddit-API-Pipeline/airflow/extraction/` called `configuration.conf`:

    ```bash
    touch ~/Reddit-API-Pipeline/airflow/extraction/configuration.conf
    ```

1. Copy the following into it:

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

    * For `aws_config` change folder into the terraform folder and run the command:


        ```bash
        terraform output
        ```
        This will output the values you need to store under `aws_config`. Just be sure to remove any `"` from the strings.
        
    * For `reddit_config` these are the details you took note of after setting up your Reddit App. Note the `developer` is your Reddit name.

---

[Previous Step](setup_infrastructure.md) | [Next Step](docker_airflow.md)

or

[Back to main README](../README.md)


# Configuration

Next, you'll need to update the configuration file with your details. The extract and load scripts will utilise the details here.

## Setup

1. Open the configuration file `~/Reddit-API-Pipeline/airflow/extraction/pipeline.conf`


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

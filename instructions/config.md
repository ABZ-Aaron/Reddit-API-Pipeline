
# Configuration

Next, you'll need to update the configuration file with your details. The extract and load scripts will utilise the details here.

## Setup

1. Open configuration file

    ```bash
    vim ~/Reddit-API-Pipeline/airflow/extraction/pipeline.conf
    ```
2. Change `XXXXX` values


    * For the Boto Config, you'll need the `access_key` and `secret_key` generated from the User Account you would have generated when you setup and configured AWS. The bucket name should be something unique (e.g. yourname-reddit-s3-bucket). The code will create this for us. The Account ID you'll find in AWS.

    * For Redshift Config, you'll need to input your Redshift `host` name, along with the `password` for the database. This is the one you specified in the previous step. The `host` name can be found in the Redshift AWS Console (it will start with the name of your cluster, and end with `amazonaws.com`). The remaining field can be left as the default assuming you set Redshift up using the `Cloudformation` script.

    * For the Reddit Config, these are the details you took note of after setting up your Reddit App. Note the `developer` is your Reddit name.

---

[Previous Step](https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/instructions/setup_redshift.md) | [Next Step](/Users/aaronwright/Documents/Tech/Projects/RedditApp/instructions/docker_airflow.md)

or

[Back to main README](../README.md)
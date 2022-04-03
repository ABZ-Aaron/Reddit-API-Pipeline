# Finishing Up

If you followed this through, congrats! You now have a functioning pipeline. If you encountered any issues along the way, please let me know so I can make improvements!

The final thing you'll probably want to do is terminate your resources, as you don't want to incur a charge for leaving your AWS resources up.

If you want to keep your pipeline running, you may be best to re-create it without using cloud computing, and something like Docker which you'll need to have running all the time. You could instead opt for a simple local PostgreSQL or SQLite database (for storage) and CRON (for orchestration).

## Termination

To terminate your resources, follow the below steps:


1. Terminate your Redshift Cluster by running the following cloudformation command. 

    ```bash
    aws cloudformation delete-stack --stack-name myredshiftstack  
    ```

    If you had issues with CloudFormation, you can instead navigate to the Redshift in the AWS Console and delete the cluster from there (be sure you have the correct region set on the top right of the UI).

    If CloudFormation is working fine for you, it's still best to double check in AWS UI that the cluster is gone.

2. Manually delete the S3 Bucket and contents. You can do this via the AWS UI in the S3 Console. Again, check the region is correct, otherwise it may appear as though you have no S3 bucket.

3. Terminate your Docker Containers. To do so, navigate to the `airflow` directory you first ran `docker-compose up` and run the following:

    ```bash
    docker-compose down
    ```

3. Delete your DBT account if necessary.

---

[Previous Step](powerbi.md)

or

[Back to main README](../README.md)

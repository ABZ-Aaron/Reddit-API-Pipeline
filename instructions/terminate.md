# Finishing Up

If you followed this through, congrats! You now have a functioning pipeline. If you encountered any issues along the way, please let me know so I can make improvements!

The final thing you'll probably want to do is terminate your resources, as you don't want to incur a charge for leaving your AWS resources up.

If you want to keep your pipeline running, you may be best to re-create it without using cloud computing, and something like Docker which you'll need to have running all the time. You could instead opt for a simple local PostgreSQL or SQLite database (for storage) and CRON (for orchestration).

## Termination

To terminate your resources, follow the below steps:


1. Terminate your Redshift Cluster by running the following Terraform command under the terraform directory:

    ```bash
    terraform destroy
    ```

    You can then check in the AWS console that Terraform has done it's job of deleting all the resources we created.




3. Terminate your Docker Containers. To do so, navigate to the `airflow` directory you first ran `docker-compose up` and run the following:

    ```bash
    docker-compose down
    ```

3. Delete your DBT account if you wish.

---

[Previous Step](powerbi.md)

or

[Back to main README](../README.md)

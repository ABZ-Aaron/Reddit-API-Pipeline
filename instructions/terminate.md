# Finishing Up

If you followed this through, congrats! You now have a functioning pipeline. If you encountered any issues along the way, please let me know so I can make improvements.

I'd recommend leaving docker running for a few days so your Redshift table contains a few day's worth of data. Or even update the reddit etl script to pull more data per run (so your dashboard looks more interesting). You can do this by changing the time filer to `week` or `all` instead of `day`.

>If you don't want to run docker running on your local machine, there are options to run it in the cloud. I provided some details on setting Docker up on an AWS EC2 in another project [here](https://github.com/ABZ-Aaron/CoinCap-API-Pipeline). You could also consider setting up a virtual machine in [Google Cloud](https://www.learningjournal.guru/article/google-cloud/free-learning-virtual-machine/). I believe the former will cost you, as AWS EC2 instances that fall under the free tier tend to be limited in memory and storage, and will likely need to be upgraded.

You'll then probably want to terminate your resources, as you don't want to incur a charge for leaving your AWS resources up. See below section for details.

>If you want to keep a dashboard up in Google Data Studio, you can change the data source to a CSV that's been downloaded from Redshift. It won't update with new data each, but is still something you can put on your resume. See previous section for details. You could also consider re-creating this pipeline without using cloud computing or Docker. You can opt for a simple local PostgreSQL or SQLite database (for storage) and CRON or Windows Task Scheduler (for orchestration). This will be free and won't drain your computer of memory & battery, while also updating your dashboard each day.

## Termination

To terminate your resources, follow the below steps:


1. Terminate your AWS resources by running the following Terraform command under the terraform directory:

    ```bash
    terraform destroy
    ```

    You can then check in the AWS console that Terraform has done it's job of deleting all the resources we created earlier.


1. Stop and delete containers, delete volumes with database data and download images. To do so, navigate to the `airflow` directory you first ran `docker-compose up` and run the following:

    ```bash
    docker-compose down --volumes --rmi all
    ```

1. The following command removes all stopped containers, all networks not used by at least one container, all unused images, all volumes, and all dangling build cache:

    ```bash
    docker system prune -a --volumes
    ```

1. Delete your DBT account if you wish, along with any EC2 instances you may have setup. 

---

[Previous Step](visualisation.md) | [Next Step](improvements.md)

or

[Back to main README](../README.md)

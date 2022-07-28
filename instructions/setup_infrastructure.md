# AWS Infrastucture <a name="SetupsRedshift"></a>

We'll use an infrastructure-as-code tool called `Terraform`. This will allow us to quickly setup (and destroy) our AWS resources using code. 

>Note that Terraform works with multiple cloud resources, not just AWS. 

If you want a quick introduction, check [this](https://learn.hashicorp.com/terraform?utm_source=terraform_io) tutorial out.

We'll use Terraform to create:

* **Redshift Cluster**

    *Redshift is a columnar data warehousing solution offered by AWS. This will be the end destination for our data.*

* **IAM Role forRedshift**

     *Role we assign to Redshift which will give it permission to read data from S3.*

* **S3 Bucket**

    *Object storage for our extracted Reddit data.*

* **Security Group**

    *This particular security group will be applied to Redshift, and will allow all incoming traffic so our dashboard can connect to it. NOTE: In a real production environment, it's not a good idea to allow all traffic into your resource.*

## Setup

1. Install Terraform 

    You can find installation instructions [here](https://learn.hashicorp.com/tutorials/terraform/install-cli) for your OS.

1. Change into `terraform` directory

    ```bash
    cd ~/Reddit-API-Pipeline/terraform
    ```

1. Open the `variables.tf` file

1. Fill in the `default` parameters.

    * Specify a master DB user password for Redshift. Note that this may show up in logs and the terraform state file. Password should contain upper and lowercase letters, as well as numbers.

    * Specify a bucket name. This should be unique and not violate any S3 bucket naming constraints (e.g. `<yourfullname>_reddit_bucket`).

    * Specify a region (e.g. `eu-west-2`). You'll find a list [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html). Ideally choose somewhere close by. 

1. May be a good idea to amend `.gitignore` to ignore all terraform files so you don't accidentally commit your password and other details. You'll need to remove the `!*.tf` line.

1. Making sure you are still in the terraform directory, run this command to download the AWS terraform plugin:

    ```bash
    terraform init
    ```

1. Run this command to create a plan based on `main.tf` and execute the planned changes to create resources in AWS:

    ```bash
    terraform apply
    ```

1. (optional) Run this command to terminate the resources:

    ```
    terraform destroy
    ```


In the [AWS Console](https://aws.amazon.com/console/), you can now view your Redshift cluster, IAM Role, and S3 Bucket. You can also manually delete or customize them here and query any Redshift databases using the query editor. Just be sure to specify the correct region in the top right hand side of the AWS console when looking for your Redshift cluster.

---

[Previous Step](aws.md) | [Next Step](config.md)

or

[Back to main README](../README.md)

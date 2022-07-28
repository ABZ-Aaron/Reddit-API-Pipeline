# AWS

We'll be using the cloud to store our Reddit data; specifically, Amazon Web Service (AWS) which offers a free tier.

We're going to be using 2 services:

* [Simple Storage Service (S3)](https://aws.amazon.com/s3/)  ~ This is Object Storage. When we extract data from Reddit, we'll store it in a CSV and push to an S3 Bucket as an object (think of a Bucket as a bit like a folder and an object as a file). This allows us to store all our raw data in the cloud.

* [Redshift](https://aws.amazon.com/redshift/) ~ This is a Data Warehousing service. Utilising its Massively Parallel Processing (MPP) technology, Redshift is able to execute operations on large datasets at fast speeds. It's based on PostgreSQL, so we can use SQL to run operations here.

In our case, we'd be fine to use a local database like PostgreSQL. However, it's good practice to work with cloud tools like this.

To get started with AWS, follow the below steps:

## Setup

1. Setup a personal [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start). Follow instructions [here](https://aws.amazon.com/getting-started/guides/setup-environment/module-one/) and setup with free tier.

2. Secure your account following these [steps](https://aws.amazon.com/getting-started/guides/setup-environment/module-two/). 

    Here we are setting up MFA for the root user. The root is a special account that has access to everything. Therefore it's important we secure this. Also be sure to setup an IAM user which will have its own set of permissions, in this case, admin permissions. Generally in production, you should only use the root account for tasks that can only be done with the root account.

3. Setup CLI following this [guide](https://aws.amazon.com/getting-started/guides/setup-environment/module-three/). 

    This allows us to control AWS services from the command line interface. The goal by the end of this is you should have a folder in your home directory called `.aws` which contains a `credentials` file. It will look something like this:

    ```config
    [default]
    aws_access_key_id = XXXX
    aws_secret_access_key = XXXX
    ```

    This will allow our scripts to interact with AWS without having to include our access key and secret access key within the scripts.

---

[Previous Step](reddit.md) | [Next Step](setup_infrastructure.md)

or

[Back to main README](../README.md)

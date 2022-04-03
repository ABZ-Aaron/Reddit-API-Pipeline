# AWS

We'll be using the cloud to store our Reddit data. In our case, we'll use Amazon Web Service (AWS) which offers a free tier.

Specifically, we're going to be using 3 services:

* [Simple Storage Service (S3)](https://aws.amazon.com/s3/)  ~ This is Cloud Storage. When we extract data from Reddit, we'll store it in a CSV and push to an S3 Bucket as an object (think of a Bucket as a folder and an object as a file). This allows us to store all our raw data in the cloud.

* [Redshift](https://aws.amazon.com/redshift/) ~ This is a Data Warehousing service. Utilising its Massively Parallel Processing (MPP) technology, Redshift is able to execute operations on large datasets at fast speeds. It's based on PostgreSQL, so we can use SQL to run these operations.

* [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html) ~ This is an infrastructure as code tool. Using CloudFormation, we can create templates which will auto-create the resources we need (e.g. Redshift Cluster).

In our case, we'd be fine to just use a local database like Postgresql. However, consider this good practice. To get started with AWS, follow the below steps:

## Setup

1. Setup a personal [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start). Follow instructions [here](https://aws.amazon.com/getting-started/guides/setup-environment/module-one/) and setup with free tier.

2. Secure your account following these [steps](https://aws.amazon.com/getting-started/guides/setup-environment/module-two/). 

    Here we are setting up MFA for the root user. The root is a special account that has access to everything. Therefore it's important we secure this. We'll also setup IAM users which will have their own set of permissions, in this case, admin permissions.

3. Setup CLI following this [guide](https://aws.amazon.com/getting-started/guides/setup-environment/module-three/). 

    This allows us to control AWS services from the command line interface. 

## Note

One thing to always note when using AWS is the region (e.g. `us-east-1`). When accessing certain resources, you can change this on the top right of the AWS UI. If you find you're missing a redshift cluster (we'll set this up next) it may be because your region isn't set to the one redshift was setup on. Change it to the correct region and you'll see your cluster.

Another thing to note, if you want to run this project fully in the cloud, you'll need to set up a virtual machine in the cloud. For AWS, this would be an [EC2](https://aws.amazon.com/ec2/instance-types/) Instance. Unfortunately, the EC2 Instance type included with the free tier is not powerful enough to run our pipeline. However, you could use a Google Cloud Virtual Machine if you wish. See [here](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12) for instructions.

---

[Previous Step](reddit.md) | [Next Step](setup_redshift.md)

or

[Back to main README](../README.md)

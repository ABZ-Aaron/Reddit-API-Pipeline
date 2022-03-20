# Reddit Pipeline

This is an independent project put together after completing a DataTalksClub [BootCamp](https://github.com/DataTalksClub/data-engineering-zoomcamp).

It is an ETL pipeline to pull Reddit data from [r/dataengineering](https://www.reddit.com/r/dataengineering/) using Reddit's API and load it into an AWS Data Warehouse.

## Architecture


## Setup AWS

1. Setup a personal [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start). Follow instructions [here](https://aws.amazon.com/getting-started/guides/setup-environment/module-one/) and setup with free tier.

2. Secure your account following these [steps](https://aws.amazon.com/getting-started/guides/setup-environment/module-two/). 

    Here we are setting up MFA for the root user. The root is a special account that has access to everything. Therefore it's important we secure this. We'll also setup IAM users which will have their own set of permissions.

3. Setup CLI following this [guide](https://aws.amazon.com/getting-started/guides/setup-environment/module-three/). 

    This allows us to control AWS services from the command line interface. We'll need to configure credentials for CLI to use.

## Setup Redshift

To setup AWS Redshift, you can use AWS's infrastructure-as-code tool `CloudFormation` by running the following steps:

```bash
git clone https://github.com/ABZ-Aaron/Reddit-API-Pipeline.git
```
* Glone git repo

```bash
cd Reddit-API-Pipeline/cloudformation
```
* Change into relevant directory

```bash
vim setup_redshift.yml
```
* Open the YML file. If vim doesn't work, open by any means you wish. Once open, update the password field with the password for the admin account setting up the cluster. Save and exit.

```bash
aws cloudformation deploy --template-file setup_redshift.yml --stack-name myredshiftstack --capabilities CAPABILITY_NAMED_IAM    
```
* Deploy redshift. This will also create an IAM Role which allows Redshift to read from S3.

If you wish to delete the resources created, run the following:

```bash
aws cloudformation delete-stack --stack-name myredshiftstack  
```

In the AWS Console, you can navigate to CloudFormation using the search bar, and check the status of your stack. If you navigate to Redshift using the search bar, you should see your cluster setup.

###



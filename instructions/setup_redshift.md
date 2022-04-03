# Redshift <a name="SetupsRedshift"></a>

As noted previously, Redshift is a columnar data warehousing solution offered by AWS. This will be the end destination for our data. Let's setup a Redshift cluster (note a cluster just describes a series of nodes).

We'll use AWS's infrastructure-as-code tool `CloudFormation`. This essentially allows us to setup AWS resources using code.

## Setup

1. Open the `setup_redshift.yml` file

    ```bash
    cd ~/Reddit-API-Pipeline/cloudformation
    vim setup_redshift.yml
    ```

2. Fill in the `MasterUserPassword` with a unique password, save, and close.

3. Run the CloudFormation AWS command.
    ```bash
    aws cloudformation deploy --template-file setup_redshift.yml --stack-name myredshiftstack --capabilities CAPABILITY_NAMED_IAM    
    ```

    This will setup a Redshift cluster, a Security Group (allows all incoming and outgoing traffic for Redshift), and an IAM Role (Allows Redshift to interact with S3). 

4. (optional) 
If you wish to terminate the resources created, run the following.

    ```bash
    aws cloudformation delete-stack --stack-name myredshiftstack  
    ```

## Note

In the AWS Console, you can navigate to `CloudFormation` using the search bar, and check the status of your stack. You can delete the resources here too. 

If you navigate to Redshift using the search bar, you should also see that your cluster is setup.

---

[Previous Step](aws.md) | [Next Step](config.md)

or

[Back to main README](../README.md)

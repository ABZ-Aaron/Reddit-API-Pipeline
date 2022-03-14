# Getting Started with AWS

I'll be setting up an EC2 Instance along with Redshift.

I will use the EC2 Instance to setup Docker & Airflow, which will be used to orchestrate the pipeline. 

I will use Redshift as a Data Warehouse solution to store Reddit data.

## Setting up AWS

1. Setup a personal [AWS account](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start). Follow instructions [here](https://aws.amazon.com/getting-started/guides/setup-environment/module-one/) and setup a free plan.

2. Secure your account following these [steps](https://aws.amazon.com/getting-started/guides/setup-environment/module-two/). 

    Here we are setting up MFA for the root user. The root is a special account that has access to everything. Therefore it's important we secure this. We'll also setup IAM users which will have their own set of permissions.

3. Setup CLI following this [guide](https://aws.amazon.com/getting-started/guides/setup-environment/module-three/). 

    This allows us to control AWS services from the command line interface. We'll need to configure credentials for CLI to use.

## Setting up EC2

An instance is a virtual server. With EC2, we can configure this server with an operating system. We can set this up with this [guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html).

When we launch an instance, we secure it with a key pair to prove our identity, and a security group. The security group acts as a firewall to control ingoing and outgoing traffic.

Once that's setup, we can connect to it via SSH. Configuration is mentioned for this [here](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12) and [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html). The second link is Amazon's instructions for connecting with SSH. The first link provides a walk through on connecting with SSH via Visual Studio code.

### Installing Requirements on EC2

We can install the necessary requirements on our EC2 following along with this video [here](https://www.youtube.com/watch?v=ae-CV2KfoN0&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=12). The video was for Google Cloud Platform, but it's the same idea. 

The general commands we'll run once connected to our instance are:

```bash
sudo yum update -y
```
* Update the package manager

#### Anaconda

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2021.11-Linux-x86_64.sh
```
* Download installation files Anaconda Distribution

```bash
bash Anaconda3-2021.11-Linux-x86_64.sh 
```
* Install Anaconda

#### Docker

```bash
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```
* Install Docker and start service, and add `ec2-user` to `docker` group so we can run docker commands without using sudo


```bash
sudo chkconfig docker on
```
* Make docker auto-start

```bash
sudo yum install -y git
```
* Install Git

```bash
sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
```
* Get latest version of docker-compose

```bash
sudo chmod +x /usr/local/bin/docker-compose
```
* Fix permissions

#### Our Files

If we have a directory we were already working on that's in GitHub we can clone this:

```bash
git clone https://github.com/ABZ-Aaron/DataEngineerZoomCamp.git
```

## Setting up Redshift


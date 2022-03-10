## Notes

### Extracting Reddit Data

To scrape Reddit data, we can use PRAW (Python Reddit API Wrapper). 

```bash
pip install praw
```

Once this is installed, we need to create a [Reddit App](https://www.reddit.com/prefs/apps) and take note of all the details.

We can then write a script to extract Reddit data. Within the script. We can import credentials for our Reddit app via a JSON file.

```python
import praw
import json

with open('extraction/secret.json', 'r') as f:
  config_data = json.load(f)

DEVELOPER = config_data['DEVELOPER']
SECRET = config_data['SECRET']
NAME = config_data['NAME']
CLIENT_ID = config_data['CLIENT_ID']

reddit_read_only = praw.Reddit(client_id=CLIENT_ID,        
                               client_secret=SECRET,
                               user_agent="My User Agent")

subreddit = reddit_read_only.subreddit("dataengineering")

print("Description:", subreddit.description)
```

### Setting up Amazon Redshift

This will be our Data Warehouse solution. We'll store our data here. This is valuable as it's fast, easy, there's no need to purchase hardware, scalable, and provides easy integration.

Essentially, Redshift is a collection of computing resources (nodes) which are organized into clusters.

Amazon Redshift has some advantages:

1. Free Basic Tier
2. Zero hardware requirements
3. Scalable
4. Easy to set up

I'll briefly explain the process of setting this up below, however here is a more detailed [guide](https://www.integrate.io/blog/data-warehousing-for-dummies-a-beginners-guide-to-setting-up-an-amazon-redshift-data-warehouse/). There are some changes which you should keep an eye out for. Make sure to select Free Trial when asked what you are planning to use this cluster for when setting up Redshift.

First step is to setup an AWS account using their [free tier](https://aws.amazon.com/free).

Secondly, we'll set up an `IAM ROLE`. This will allow us to access data from AWS instances called Amazon Simple Storage Service (S3) buckets. 

These are like folders in the AWS ecosystem, containing data and metadata. 

The IAM role provides a data connection, so that our Redshift cluster can access the data in our buckets. 

We then want to setup a Redshift cluster.

### Amazon S3

S3 is AWS's cloud storage solution, accessible from anywhere in the world.

Main components of S3 are buckets and objects. Buckets are like folders. Objects are like files.

Buckets have permissions policies. They can act as folders, generate logs, and contain objects. The objects can be images, CSV files, and so on.

We can create buckets, list buckets, and delete buckets. 

First we create our client:

```python
impot boto3
s3 = boto3.client('s3', AWS_ACCESS_KEY_ID = "", AWS_SECRET_ACCESS_KEY = "")
```

To create bucket with boto3:

```python
bucket = s3.create_bucket(Bucket = 'my_bucket')
```

Bucket names have to be unique across all of S3

To list our buckets:

```python
bucket_response = s3.list_buckets()
buckets = bucket_response['Buckets']
```

To delete a bucket:

```python
response = s3.delete_bucket('my_bucket')
```

To list our buckets:

```python
listing = s3.list_buckets()
```

An objects key is the full path from the full path from bucket root. An object can only belong to one bucket. 

To upload file to a bucket with a defined name (key):

```python
s3.upload_file(Filename = '', Bucket = '', Key = '')
```

To list objects in a bucket, limiting the amount returned:

```python
response = s3.list_objects(Bucket = '', MaxKeys = '', Prefix = '')
```

To download file from bucket:

```python
s3.download_file(Filename = '', Bucket = '', Key = '')
```

To delete:

```python
s3.delete_object(Bucket = '', Key = '')
```

To get metadata:

```python
response = s3.head_object(Bucket='', Key='')
```
# Data Visualisation 

We now want to visualise our data. It's up to you how to do this. 

Below I've provided some basic instructions on connecting Redshift to [PowerBI](https://powerbi.microsoft.com/en-gb/) and [Google Data Studio](https://datastudio.google.com).

Feel free to use the default table in Redshift (i.e. reddit) or the newly transformed one we created with dbt (i.e. reddit_transformed).

> Google Data Studio is the better option for a personal project, as reports created here can freely and easily be shared.

## Google Data Studio

1. Navigate [here](https://datastudio.google.com) and follow the setup instructions. 
1. Click `Create` on the top right, then `Report`
1. Under `Connect to data` search for `Amazon Redshift`
1. Enter the relevant details and click `Authenticate`
1. Select your table

You can now feel free to create some visualisations. Some tutorial/guides [here](https://support.google.com/datastudio/answer/6283323?hl=en). Here's an example of mine:

[<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/GDS-Dashboard.png" width=70% height=70%>](https://datastudio.google.com/reporting/e927fef6-b605-421c-ae29-89a66e11ea18)

You can then publicly share your report by navigating to Share > Manage access.

### What to do once resources are terminated

One thing to note... you don't want to keep your Redshift cluster up past 2 months, as it'll incur a cost once the free trial period comes to an end. You also probably don't want the Airflow Docker containers running on your local machine all the time as this will drain resources and memory.

As such, your Redshift-Google Data Studio connection will eventually be broken. If you want to display a dashboard on your resume even after this happens, one option is to download your Redshift as a CSV as use this as the data source in Google Data Studio:

1. Run the `download_redshift_to_csv.py` file under the `extraction` folder to download your Redshift table as a CSV to your `/tmp` folder. Store this CSV somewhere safe. If you want to download the transformed version of your table, you may need to amend this script slightly to include the new table name, as well as the schema.
1. If you've already created your report in Google, try navigating to File > Make a copy, and select the CSV as the new data source. This should maintain all your existing visualisations.
1. You could also refactor the pipeline to use [CRON](https://en.wikipedia.org/wiki/Cron) and [PostgreSQL](https://www.postgresql.org). You could leave this pipeline running as long as you want without incurring a charge, and your Google Data Studio report will be continuously updated with new data.

## PowerBI

For PowerBI, you'll need to use Windows OS and install PowerBI Desktop. If you're on Mac or Linux, you can consider a virtualisation software like [virtualbox](https://www.virtualbox.org) to use Windows.

To connect Redshift to PowerBI:
 
1. Create an account with PowerBI. If you don't have a work or school email address, consider setting up an account with a [temporary email address](https://tempmail.net), as it won't accept Gmail and other services used for personal accounts. 
1. Open PowerBI and click `Get Data`.
1. Search for `Redshift` in the search box and click `Connect`.
1. Enter your Redshift server/host name, and the name of the database (e.g. dev) and click `OK`.
1. Enter the username (e.g. awsuser) and password for the database, and then select the relevant table you'd like to load in. 

You can now feel free to create some visualisations. Some tutorials/guides [here](https://docs.microsoft.com/en-us/learn/powerplatform/power-bi).

---

[Previous Step](dbt.md) | [Next Step](terminate.md)

or

[Back to main README](../README.md)

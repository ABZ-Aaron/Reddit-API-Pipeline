# Data Visualisation 

We now want to visualise our data. I'll leave it to you how you want to do this, but see below for some basic instructions on connecting Redshift to [PowerBI](https://powerbi.microsoft.com/en-gb/). 

For this, you'll need to use Windows OS. If you're on Mac or Linux, you can consider a virtualisation software like [virtualbox](https://www.virtualbox.org) to use Windows.

If that's not an option, other BI tools won't differ too much from PowerBI, and connecting Redshift will be much the same as it is for PowerBI.

## Setup

To connect Redshift to PowerBI:

1. Create an account with PowerBI. If you don't have a work or school email address, consider setting up an account with a [temporary email address](https://tempmail.net), as it won't accept Gmail and other services used for personal accounts. 

2. Open PowerBI and click `Get Data`
3. Search for `Redshift` in the search box and click `Connect`
4. Enter your Redshift server/host name, and the name of the database (e.g. dev) and click `OK`
5. Enter the username (e.g. awsuser) and password for the database, and then select the relevant table you'd like to load in. 
6. You can now feel free to create some graphs and visualisations. Here's an example:

  <img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/dashboard2.png" width=70% height=70%>


  <img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/dashboard1.png" width=70% height=70%>

---

[Previous Step](dbt.md) | [Next Step](terminate.md)

or

[Back to main README](../README.md)

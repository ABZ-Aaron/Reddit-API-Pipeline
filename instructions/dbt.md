# DBT

dbt (data build tool) is a transformation tools that sits on top of our data warehouse.

We don't actually require any real transformation on our data; however, like before, consider this good practice. There is a bit of setup required here, so feel free to skip this if you just want to see your Redshift data in Google Data Studio.

In production, this could be used to create multiple different tables with different columns. Data scientists might be given access to one table, and data analysts the other, as an example. dbt would be able to run tests when creating these new tables, produce documentation for analysts to examine, help manage dependencies between models, and so forth.

If you continue, I'd recommend taking a quick look at some dbt [tutorials](https://docs.getdbt.com/docs/dbt-cloud/cloud-quickstart). I'll only go through some basic steps to setup a transformation here.

For reference, here's a [link](https://github.com/ABZ-Aaron/Reddit-API-Pipeline-DBT) to the separate repo I set up for dbt.

## Setup (development)

1. Create a dbt account [here](https://www.getdbt.com/signup/).

1. Create a project or just stick to the default project created.

1. Setup Up a `Database Connection` - Select Redshift

1. On the next page, enter the relevant Redshift details. This includes the `hostname`. You'll find this in the AWS Redshift console, or from the `terraform output` command mentioned earlier. It will start with the name of your cluster and end with `amazonaws.com`. It will also require the port (likely `5439`), the database name (likely `dev`). You'll also need the database username (likely `awsuser`) and password for the database you specified in the `Terraform` step. Once everything is input, click the `Test` button at the top. If successful, click `Continue`. 

1. Once connection is established, choose `managed directory` and give it  a name. You can also choose Github if you have a Github repo setup for the dbt part of this project, like I have, although this will require a bit of configuration.

1. Once you've worked through these initial steps, click on `Start Developing`.

You are now in an IDE which is connected to your Redshift cluster. Here we'll run some basic transformations on our data.

1. Click on `initialize project`. This will populate the directory on the left hand side with folder and files we may need.

1. Under the `models` folder, create new files called `reddit_transformed.sql` (this name will be the name of the new model you create) and `schema.yml`. You can delete the `example` folder.

1. In the `schema.yml` file, copy the following and save. Here we are defining some basic tests and documentation for our table. I haven't added much, as it's mostly for demonstration purposes. You can see that I've added a `not_null` test for `id`. For the rest, I've only added in the name of the column and a description.

    ```yaml
    version: 2

    models:
      - name: reddit_transformed
        description: Transformed Reddit Data
        columns:
          - name: id
            description: Reddit ID of Post
            tests:
              - not_null
          - name: title
            description: Title of Reddit Post
          - name: text
            description: Body Text of Reddit Post
          - name: score
            description: Score of Reddit Post
          - name: comments
            description: Number of Comments for Post
          - name: url
            description: Full URL of Reddit Post
          - name: comment
            description: Top comment for Reddit Post
          - name: dateposted
            description: Date Reddit Data was Downloaded
    ```
1. In the `text_posts.sql` file, copy the following and save. This wil be our only transformation. This is basically removing some columns that don't really need, and also splitting the UTC datetime column into `utc_date` and `utc_time`. Feel free to transform the data in whichever way you want. This is just a VERY basic example.

    ```SQL
    SELECT id, 
       title, 
       num_comments, 
       score,
       author,
       created_utc,
       url,
       upvote_ratio,
       created_utc::date as utc_date,
       created_utc::time as utc_time
    FROM dev.public.reddit
    ```

1. If you check the bottom right of the screen, you'll see a preview button. Click this to see what your outputted table will look like based on the above SQL query. Basically, when we run `dbt run` in the UI (further down this page) what'll happen is this table will be created in a new schema within our Redshift database.

1. Under the `dbt_project.yml`, update it to the following. All we've really changed here is the project name to `reddit_project` and told dbt to create all models as tables (rather than views). You can leave it as views if you wish.

    ```yaml
    # Name your project! Project names should contain only lowercase characters
    # and underscores. A good package name should reflect your organization's
    # name or the intended use of these models
    name: 'reddit_project'
    version: '1.0.0'
    config-version: 2

    # This setting configures which "profile" dbt uses for this project.
    profile: 'default'

    # These configurations specify where dbt should look for different types of files.
    # The `source-paths` config, for example, states that models in this project can be
    # found in the "models/" directory. You probably won't need to change these!
    model-paths: ["models"]
    analysis-paths: ["analyses"]
    test-paths: ["tests"]
    seed-paths: ["seeds"]
    macro-paths: ["macros"]
    snapshot-paths: ["snapshots"]

    target-path: "target"  # directory which will store compiled SQL files
    clean-targets:         # directories to be removed by `dbt clean`
      - "target"
      - "dbt_packages"


    # Configuring models
    # Full documentation: https://docs.getdbt.com/docs/configuring-models

    # In this example config, we tell dbt to build all models in the example/ directory
    # as tables. These settings can be overridden in the individual model files
    # using the `{{ config(...) }}` macro.
    models:
      reddit_project:
        materialized: table
    ```

1. To test what we've done, we can run the following commands at the bottom of the DBT IDE and make sure an error isn't returned:

    ```bash
    dbt run
    ```
      
    ```bash
    dbt test
    ```

1. `dbt run` will generate our table within a different schema in Redshift. Easiest way to see this is to navigate to the AWS Console, login, search for Redshift, and use the Query Editor V2. `dbt test` will check the new model passes the tests (or test in our case) specified in the `schema.yml` file.

1. The next step is to click `commit` on the left hand menu to commit our changes.


If you ran `dbt run` above and no error was returned, a new table will have been created in our Redshift database, under a new schema name. You would have specified this schema name during the initial setup of dbt during the Redshift connection phase. If you left it as the default, it'll likely be something like `dbt_<dbt user name>`.

To check this, navigate to your Redshift cluster in AWS, and click on Query Data on the top right (orange button). Here, you want to navigate to the `dev` database, select the relevant schema, and check that the new table is there. You can query it with:

```sql
SELECT * FROM <schema name>.reddit_transformed;
```

<img src="https://github.com/ABZ-Aaron/Reddit-API-Pipeline/blob/master/images/redshift.png" width=70% height=70%>

## Setup (production)

When you working in your DBT development environment, this is where the models are created.

However, consider this schema to be our development environment. We now want to setup a production run, as we wouldn't want analysts accessing our models from within our development area.

1. To do this, navigate to the left hand side menu and select `Environments` then click `New Environments`.

1. The `Type` option should be set to `Deployment`. Change the `Name` to something like `Production Run`.
1. Under `Deployment Credentials` enter your database username and password again. Also set a schema name, something like `Analytics`, and Save.
1. Click on `New Job`.
1. Give your job a name. Set environment as the `Production Run` you just created.
1. Select the `Generate Docs` radio button.
1. Under `Commands` ensure that `dbt run` and `dbt test` are both there.
1. Under `Triggers` ,normally you'd have this on a schedule, but for our purposes, just de-select so that it does not run on a schedule. We'll just run it manually for now.
1. Scroll to the top and save. Once saved, click `Run Now`. After a minute or two, you can then check the Redshift cluster, where you should find a new schema folder with our production table/model!

---

[Previous Step](docker_airflow.md) | [Next Step](visualisation.md)

or

[Back to main README](../README.md)

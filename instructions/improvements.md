# Improvements

These are some improvements that could be made.

## Setup Alerts & Notifications

With Airflow, we can have it send emails when there has been a failure.

## Improve Airflow & Docker process

Docker/Aiflow files used were pulled from online with very few changes made. These could be simplified and/or refactored with a real production environment in mind.

## Testing & Validation

Better validation checks could be implemented to check data is correct, check all components of the pipeline work together and on their own, remove duplicates, and so forth.

## Simplify Process

The use of Airflow and dbt is overkill. Alternative ways to run this pipeline could be with Cron for orchestration and PostgreSQL or SQLite for storage.

## Stream over Batch Processing

If we want our Dashboard to always be up-to-date, we could benefit from something like Kafka.

## Optimisation

Look for performance improvements, reduce code redundancy, and implement software engineering best practices. For example, consider using Parquet file format over CSV, or consider whether warehouse data could be modeled as a star schema.

[Previous Step](terminate.md)

or

[Back to main README](../README.md)



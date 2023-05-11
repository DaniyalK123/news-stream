# News Article Data Pipeline

This is a slightly modified version of a project for an event processing course.

This project is a streaming data pipeline for news articles that extracts data from the News API, processes it, and stores the processed data in mini star schema in BigQuery. The pipeline consists of three main components: API ingestion, Apache Beam for data processing, and DBT for data transformation.

## Components

1. **API Ingestion**: A Python script that fetches news articles based on specific keywords from the News API and publishes the data to Google Cloud Pub/Sub.
2. **Apache Beam**: A Dataflow pipeline that reads the data from Google Cloud Pub/Sub, processes it (including sentiment analysis and deduplication), and writes the results to BigQuery.
3. **DBT**: A DBT project that transforms the raw data in BigQuery into a star schema with fact and dimension tables.



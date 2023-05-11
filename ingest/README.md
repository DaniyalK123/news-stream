# API Ingestion

This folder contains the Python script used for fetching news articles from the News API and publishing the data to Google Cloud Pub/Sub.

## Usage

1. Set up the required environment variables:
   - `NEWS_API_KEY`: Your News API key.
   - `GOOGLE_APPLICATION_CREDENTIALS`: The path to your Google Cloud service account key file.
   - `PUBSUB_TOPIC`: The Pub/Sub topic to publish the messages to.

2. Install the required Python packages:


3. Run the Python script with the desired keywords as comma-separated command line arguments e.g `python main.py "keyword1,keyword2,keyword3"`

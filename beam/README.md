# Apache Beam Data Processing

This folder contains the Apache Beam pipeline code that processes the news articles fetched from the News API.

## Usage

1. Set up the required environment variables:
   - `GOOGLE_APPLICATION_CREDENTIALS`: The path to your Google Cloud service account key file.

2. Install the required Python packages: pip install -r requirements.txt


3. Run the Apache Beam pipeline using the Dataflow runner:

'''
python main.py \
  --input_topic "projects/$GCP_PROJECT_ID/topics/$INPUT_TOPIC" \
  --output_table "$GCP_PROJECT_ID:$GCP_RAW_TABLE" \
  --project $GCP_PROJECT_ID \
  --region $GCP_REGION \
  --zone $GCP_ZONE
  --temp_location $TEMP_LOCATION
'''

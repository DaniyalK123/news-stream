import argparse
import os
import json
import requests
import datetime
from google.cloud import pubsub_v1

API_KEY = os.environ.get('NEWS_API_KEY')
NEWS_API_URL = 'https://newsapi.org/v2/everything'
PUBSUB_PROJECT_ID = os.environ.get('GCP_PROJECT_ID')
PUBSUB_TOPIC = os.environ.get('GCP_PUBSUB_TOPIC')
LAST_RUN_FILE = 'last_run.txt'

def save_last_run_time(timestamp):
    with open(LAST_RUN_FILE, 'w') as file:
        file.write(str(timestamp))

def load_last_run_time():
    if os.path.exists(LAST_RUN_FILE):
        with open(LAST_RUN_FILE, 'r') as file:
            return datetime.datetime.fromisoformat(file.read()).strftime("%Y-%m-%d")
    return None


def fetch_articles(keywords, from_time):
    query = f'{" OR ".join(keywords)}'
    params = {
        'apiKey': API_KEY,
        'q': query,
        'from': from_time,
        'sortBy': 'publishedAt',
        'pageSize': 100
    }
    print(params)
    all_articles = []
    page = 1
    MAX_PAGES = 1
    c = 0
    while c < MAX_PAGES:
        c += 1
        params['page'] = page
        response = requests.get(NEWS_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            all_articles.extend(data['articles'])
            if page * 100 >= data['totalResults']:
                break
            page += 1
        else:
            print(f"Error {response.status_code}: {response.text}")
            break
    return all_articles


def create_pubsub_publisher():
    return pubsub_v1.PublisherClient()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("keywords", help="Comma-separated keywords to fetch articles")
    args = parser.parse_args()
    keywords = args.keywords.split(',')

    last_run_time = load_last_run_time()
    if last_run_time is None:
        last_run_time = (datetime.datetime.now() - datetime.timedelta(hours=24)).strftime("%Y-%m-%d")

    articles = fetch_articles(keywords, last_run_time)

    publisher = create_pubsub_publisher()
    topic_path = publisher.topic_path(PUBSUB_PROJECT_ID, PUBSUB_TOPIC)
    

    for article in articles:
        data = json.dumps(article).encode('utf-8')
        future = publisher.publish(topic_path, data=data)
        message_id = future.result()
        print(f"Published message ID: {message_id}")

    


    save_last_run_time(datetime.datetime.now())



if __name__ == '__main__':
    main()

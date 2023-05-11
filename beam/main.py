import argparse
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.io import ReadFromPubSub, WriteToBigQuery
from textblob import TextBlob
from langdetect import detect


class DeserializeJson(beam.DoFn):
    def process(self, element):
        try:
            return [json.loads(element)]
        except json.JSONDecodeError:
            return []
        

class DeduplicateURL(beam.PTransform):
    def expand(self, pcoll):
        return (
            pcoll
            | "Key by URL" >> beam.WithKeys(lambda x: x["url"])
            | "Windowing" >> beam.WindowInto(beam.window.FixedWindows(1000000),
                                               trigger=beam.trigger.Repeatedly(
                                                   beam.trigger.AfterCount(1)),
                                               accumulation_mode=beam.trigger.AccumulationMode.DISCARDING)
            | "Group by URL" >> beam.GroupByKey()
            | "Take first element of grouped URLs" >> beam.Map(lambda x: x[1][0])
        )

class AddSentimentScore(beam.DoFn):
    def process(self, element):
        text = element['title'] + ' ' + element['description']
        sentiment_score = TextBlob(text).sentiment.polarity
        element['sentiment_score'] = sentiment_score
        return [element]


class AddWordCount(beam.DoFn):
    def process(self, element):
        text = element['title'] + ' ' + element['description']
        word_count = len(text.split())
        element['word_count'] = word_count
        return [element]


class AddLanguage(beam.DoFn):
    def process(self, element):
        try:
            language = detect(element['title'])
        except:
            language = 'unknown'
        element['language'] = language
        return [element]


def run(argv=None, save_main_session=True):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input_topic',
        help='The Cloud Pub/Sub topic to read from.',
        required=True)
    parser.add_argument(
        '--output_table',
        help='The BigQuery table to write the results to.',
        required=True)
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    google_cloud_options = pipeline_options.view_as(GoogleCloudOptions)
    pipeline_options.view_as(beam.options.pipeline_options.StandardOptions).streaming = True
    pipeline_options.view_as(StandardOptions).runner = 'DataflowRunner'

    with beam.Pipeline(options=pipeline_options) as p:
        (p | 'ReadFromPubSub' >> ReadFromPubSub(topic=known_args.input_topic)
           | 'DeserializeJson' >> beam.ParDo(DeserializeJson())
           | 'Deduplicate by URL' >> DeduplicateURL()
           | 'AddSentimentScore' >> beam.ParDo(AddSentimentScore())
           | 'AddWordCount' >> beam.ParDo(AddWordCount())
           | 'AddLanguage' >> beam.ParDo(AddLanguage())
           | 'WriteToBigQuery' >> WriteToBigQuery(
               known_args.output_table,
               schema='source_id:STRING, source_name:STRING, author:STRING, '
                      'title:STRING, description:STRING, url:STRING, '
                      'urlToImage:STRING, publishedAt:STRING, content:STRING, '
                      'sentiment_score:FLOAT, word_count:INT64, language:STRING',
               write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND))


if __name__ == '__main__':
    run()


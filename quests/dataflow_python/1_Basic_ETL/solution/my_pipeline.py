import argparse
import time
import logging
import json
import apache_beam as beam
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.runners import DataflowRunner, DirectRunner

# ### main

def run():
    # Command line arguments
    # parser = argparse.ArgumentParser(description='Load from Json into BigQuery')
    # parser.add_argument('--project',required=True, help='Specify Google Cloud project')
    # parser.add_argument('--region', required=True, help='Specify Google Cloud region')
    # parser.add_argument('--stagingLocation', required=True, help='Specify Cloud Storage bucket for staging')
    # parser.add_argument('--tempLocation', required=True, help='Specify Cloud Storage bucket for temp')
    # parser.add_argument('--runner', required=True, help='Specify Apache Beam Runner')

    # opts = parser.parse_args()

    # # Setting up the Beam pipeline options
    # options = PipelineOptions()
    # options.view_as(GoogleCloudOptions).project = opts.project
    # options.view_as(GoogleCloudOptions).region = opts.region
    # options.view_as(GoogleCloudOptions).staging_location = opts.stagingLocation
    # options.view_as(GoogleCloudOptions).temp_location = opts.tempLocation
    # options.view_as(GoogleCloudOptions).job_name = '{0}{1}'.format('my-pipeline-',time.time_ns())
    # options.view_as(StandardOptions).runner = opts.runner

    args = [
        '--project=prj-gmms-sandbox-s-36ac',
        '--region=us-central1',
        '--runner=DataflowRunner',
        # '--runner=DirectRunner',
        '--staging_location=gs://prj-gmms-sandbox-s-36ac/staging',
        '--temp_location=gs://prj-gmms-sandbox-s-36ac/temp/',
        '--subnetwork=https://www.googleapis.com/compute/v1/projects/prj-pp-gen-preprod-net-acc7/regions/us-central1/subnetworks/sb-vpc-pp-gen-preprod-us-central1-0',
        '--service_account_email=sa-gmms-sandbox-s-dflow@prj-gmms-sandbox-s-36ac.iam.gserviceaccount.com',
        '--no_use_public_ips',
    ]

    # Static input and output
    input='gs://prj-gmms-sandbox-s-36ac/events.json'
    output='prj-gmms-sandbox-s-36ac:logs.logs'

    # Table schema for BigQuery
    table_schema = {
        "fields": [
            {
                "name": "ip",
                "type": "STRING"
            },
            {
                "name": "user_id",
                "type": "STRING"
            },
            {
                "name": "lat",
                "type": "FLOAT"
            },
            {
                "name": "lng",
                "type": "FLOAT"
            },
            {
                "name": "timestamp",
                "type": "STRING"
            },
            {
                "name": "http_request",
                "type": "STRING"
            },
            {
                "name": "http_response",
                "type": "INTEGER"
            },
            {
                "name": "num_bytes",
                "type": "INTEGER"
            },
            {
                "name": "user_agent",
                "type": "STRING"
            }
        ]
    }

    # Create the pipeline
    p = beam.Pipeline(argv=args)

    '''

    Steps:
    1) Read something
    2) Transform something
    3) Write something

    '''

    (p
        | 'ReadFromGCS' >> beam.io.ReadFromText(input)
        | 'ParseJson' >> beam.Map(lambda line: json.loads(line))
        | 'WriteToBucket' >> beam.io.WriteToText('gs://prj-gmms-sandox-psa-s-36ac/outputData')
        # | 'WriteToBQ' >> beam.io.WriteToBigQuery(
        #     output,
        #     schema=table_schema,
        #     create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
        #     write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
        #     )
    )

    logging.getLogger().setLevel(logging.INFO)
    logging.info("Building pipeline ...")

    p.run()

if __name__ == '__main__':
  run()

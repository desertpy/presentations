import os
import sys
import subprocess
import uuid
import boto3

libdir = os.path.join(os.getcwd(), 'local', 'lib')
s3_client = boto3.client('s3')

def handler(event, context):
    results = []
    for record in event['Records']:

        # Find input/output buckets and key names
        bucket = record['s3']['bucket']['name']
        output_bucket = "{}-geojson".format(bucket)
        key = record['s3']['object']['key']
        output_key = "{}.geojson".format(key)

        # Download the raster locally
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), key)
        s3_client.download_file(bucket, key, download_path)

        # Call the worker, setting the environment variables
        command = 'LD_LIBRARY_PATH={} python worker.py {}'.format(libdir, download_path)
        output_path = subprocess.check_output(command, shell=True)

        # Upload the output of the worker to S3
        s3_client.upload_file(output_path.strip(), output_bucket, output_key)
        results.append(output_path.strip())

    return results

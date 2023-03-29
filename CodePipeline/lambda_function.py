import json
import os
import logging
import boto3
import requests
from datetime import datetime
from requests_aws4auth import AWS4Auth

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

region = 'us-east-1'
service = 'es'
credentials = boto3.Session().get_credentials()

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

rekognition = boto3.client('rekognition')


def lambda_handler(event, context):
    records = event['Records']

    for record in records:
        s3object = record['s3']
        bucket = s3object['bucket']['name']
        objectKey = s3object['object']['key']

        print(s3object)
        print(bucket)
        print(objectKey)

        image = {
            'S3Object': {
                'Bucket': bucket,
                'Name': objectKey
            }
        }

        response = rekognition.detect_labels(Image=image)
        labels = list(map(lambda x: x['Name'], response['Labels']))
        timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

        # print out the labels
        print(labels)

        es_endpoint = 'https://search-photo-search-d7qcrc4oxwpstfmjnbvcbhvgcq.us-west-2.es.amazonaws.com'
        es_index = 'photo-search'
        es_type = '_doc'

        es_url = f'{es_endpoint}/{es_index}/{es_type}'

        es_data = {
            'objectKey': objectKey,
            'bucket': bucket,
            'createdTimesatamp': timestamp,
            'labels': labels
        }

        es_headers = {
            'Content-Type': 'application/json'
        }

        es_response = requests.post(
            es_url,
            auth=awsauth,
            headers=es_headers,
            json=es_data
        )

        logger.debug(f'ES response: {es_response.text}')

    return {
        'statusCode': 200,
        'body': json.dumps('Indexed photos successfully done.')
    }

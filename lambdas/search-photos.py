import json
import math
import dateutil.parser
import datetime
import time
import os
import logging
import boto3
import uuid
import requests
import urllib.parse
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

headers = {"Content-Type": "application/json"}
host = 'https://search-photo-search-d7qcrc4oxwpstfmjnbvcbhvgcq.us-west-2.es.amazonaws.com/'
region = 'us-west-2'
# Create a Lex V2 Runtime client
lex_client = boto3.client("lexv2-runtime")

# Generate a unique ID for the user
user_id = str(uuid.uuid4())


def lambda_handler(event, context):
    print('event : ', event)

    q1 = event["queryStringParameters"]['q']

    # if(q1 == "searchAudio" ):
    #     q1 = convert_speechtotext()

    print("q1:", q1)
    labels = get_labels(q1)
    print("labels", labels)
    img_paths = []
    if len(labels) != 0:
        img_paths = get_photo_path(labels)

    if not img_paths:
        return {
            'statusCode': 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps('No Results found')
        }
    else:
        return {
            'statusCode': 200,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': {
                'imagePaths': img_paths,
                'userQuery': q1,
                'labels': labels,
            },
            'isBase64Encoded': False
        }


def get_labels(query):
    response = lex_client.recognize_text(
        botAliasId="TSTALIASID",
        botId="I1YDNCYLAC",
        localeId="en_US",
        sessionId=user_id,
        text=query,
    )

    print("lex-response", response)

    labels = []
    if 'slots' not in response:
        print("No photo collection for query {}".format(query))
    else:
        print("slot: ", response['slots'])
        slot_val = response['slots']
        for key, value in slot_val.items():
            if value != None:
                labels.append(value)
    return labels


def get_photo_path(keys):
    es = Elasticsearch(
        [host],
        http_auth=("admin", "WYHram1220$"),
    )

    resp = []
    for key in keys:
        if (key is not None) and key != '':
            searchData = es.search({"query": {"match": {"labels": key}}})
            resp.append(searchData)
    print(resp)
    output = []
    for r in resp:
        if 'hits' in r:
            for val in r['hits']['hits']:
                key = val['_source']['objectKey']
                if key not in output:
                    output.append('https://s3.us-west-2.amazonaws.com/imgorig/' + key)
    print(output)
    return output

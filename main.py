#!/usr/bin/env python

from os import getenv
from google.cloud import storage
from flask import send_file

# Global values
BUCKET_NAME = getenv('BUCKET_NAME', 'playground-s-11-ff0529c4-bpo')
FILE_NAME = getenv('FILE_NAME', 'EXPORT.csv')
TEMP_PATH = getenv('TEMP_PATH', '/tmp')


def download_file(request):
    """
    List all blobs in the bucket
    :param request: Cloud function request
    :return: result
    """

    # CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Authorization',
            'Access-Control-Max-Age': '3600',
            'Access-Control-Allow-Credentials': 'true',
        }
        return '', 204, headers

    # Set CORS headers for main requests
    # headers = {
    #     'Access-Control-Allow-Origin': '*',
    #     'Access-Control-Allow-Credentials': 'true',
    # }

    # Create client
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(FILE_NAME)
    # Download
    temp_file = f'{TEMP_PATH}/{FILE_NAME}'
    blob.download_to_filename(temp_file)

    return send_file(temp_file, mimetype='text/csv', download_name=FILE_NAME, as_attachment=True)

import json
import boto3
from PIL import Image
import os
import urllib.parse

s3 = boto3.client('s3')

DEST_BUCKET = 'capstone-image-resizer-output'
WIDTH = 300
HEIGHT = 300

def lambda_handler(event, context):
    
    # Get file info
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    download_path = '/tmp/' + os.path.basename(key)
    upload_path = '/tmp/resized-' + os.path.basename(key)

    # Download image
    s3.download_file(bucket, key, download_path)

    # Resize image
    with Image.open(download_path) as img:
        img = img.resize((WIDTH, HEIGHT))
        img.save(upload_path)

    # Upload resized image
    s3.upload_file(upload_path, DEST_BUCKET, 'resized-' + key)

    return {
        'statusCode': 200,
        'body': json.dumps('Image resized successfully!')
    }
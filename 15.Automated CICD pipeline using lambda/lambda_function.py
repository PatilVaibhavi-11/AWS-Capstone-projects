import json
import boto3
import zipfile
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Get artifact details from CodePipeline
        job_id = event['CodePipeline.job']['id']
        artifact = event['CodePipeline.job']['data']['inputArtifacts'][0]
        
        s3_location = artifact['location']['s3Location']
        bucket = s3_location['bucketName']
        key = s3_location['objectKey']

        # Download artifact
        download_path = '/tmp/source.zip'
        s3.download_file(bucket, key, download_path)

        # Extract files
        extract_path = '/tmp/extracted'
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Upload to deployment bucket
        deploy_bucket = 'my-cicd-deploy-bucket'

        for root, dirs, files in os.walk(extract_path):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, extract_path)

                s3.upload_file(full_path, deploy_bucket, relative_path)

        return {
            'statusCode': 200,
            'body': json.dumps('Deployment Successful')
        }

    except Exception as e:
        print(str(e))
        raise e
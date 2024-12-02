import json
import boto3
import zipfile
import io
import os
from typing import Dict, Any

s3_client = boto3.client("s3")
TARGET_BUCKET_NAME = os.environ.get("TARGET_BUCKET_NAME")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        # Get bucket and key from the S3 event
        source_bucket = event["Records"][0]["s3"]["bucket"]["name"]
        zip_key = event["Records"][0]["s3"]["object"]["key"]

        # Define target bucket for decompressed files
        target_bucket = os.environ.get(TARGET_BUCKET_NAME, source_bucket)

        # Download the zip file from S3 into memory
        zip_obj = s3_client.get_object(Bucket=source_bucket, Key=zip_key)
        buffer = io.BytesIO(zip_obj["Body"].read())

        # Process the zip file
        with zipfile.ZipFile(buffer) as zip_ref:
            # Iterate through all files in the zip
            for file_name in zip_ref.namelist():
                # Read the file content from zip
                with zip_ref.open(file_name) as file:
                    content = file.read()

                    # Upload the file to S3
                    target_key = f"decompressed/{''.join(str.split(os.path.basename(zip_key),'.')[:-1])}/{file_name}"
                    s3_client.put_object(
                        Bucket=target_bucket, Key=target_key, Body=content
                    )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Successfully decompressed files",
                    "source_bucket": source_bucket,
                    "source_key": zip_key,
                    "target_bucket": target_bucket,
                }
            ),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {"message": "Error processing zip file", "error": str(e)}
            ),
        }

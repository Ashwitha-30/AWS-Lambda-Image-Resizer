import boto3
from PIL import Image
import io

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        try:
            # Download image
            response = s3_client.get_object(Bucket=bucket, Key=key)
            file_content = response['Body'].read()

            # Open image using Pillow (detects format automatically)
            img = Image.open(io.BytesIO(file_content))
            img_format = img.format  # 'PNG', 'JPEG', etc.

            # Resize
            img = img.resize((200, 200))
            buffer = io.BytesIO()
            img.save(buffer, format=img_format)
            buffer.seek(0)

            # Upload to another bucket
            s3_client.put_object(
                Bucket="ashu-image-upload-resized",
                Key=key,
                Body=buffer,
                ContentType=f"image/{img_format.lower()}"
            )

            print(f"Successfully resized {key}")

        except Exception as e:
            print(f"Error processing file {key}: {e}")

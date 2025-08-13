## Step 1 — Create an S3 Bucket for Original Images
Open AWS Console → S3.

Click Create bucket → Name: my-original-images-bucket.

Region: choose same as Lambda will be in.

Leave other settings default → Create bucket.
------------------------------------------------------------

## Step 2 — Create an S3 Bucket for Resized Images
Create another bucket: my-resized-images-bucket.

Keep default settings → Create bucket.
-------------------------------------------------------------

## Step 3 — Create IAM Role for Lambda
Go to IAM → Roles → Create role.

Select AWS service → Lambda.

Attach policies:

AmazonS3FullAccess ✅

CloudWatchLogsFullAccess ✅

Name it: lambda-s3-fullaccess-role → Create role.
----------------------------------------------------------------

## Step 4 — Prepare Python Code on Linux
On your Ubuntu/Linux terminal:

mkdir image-resizer
cd image-resizer
nano lambda_function.py
Paste this code (Python 3.12):


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



Save & exit → CTRL+O, ENTER, CTRL+X.
-----------------------------------------------------------------------------------------

## Step 5 — Install Pillow & Create Zip Files
Still in terminal:

mkdir python
pip install pillow -t python/
zip -r pillow-layer.zip python
zip function-code.zip lambda_function.py
Now you have:

pillow-layer.zip → Layer for image processing.

function-code.zip → Your Lambda code.
-----------------------------------------------------------------------------------------

## Step 6 — Create Lambda & Add Code
In AWS Console → Lambda → Create function.

Name: image-resizer-func.

Runtime: Python 3.12

Role: Choose existing → lambda-s3-fullaccess-role.

Create function.

In Code → Upload from .zip → Select function-code.zip.

Deploy.
-------------------------------------------------------------------------------------------

## Step 7 — Add Pillow Layer
In Lambda → Layers → Create layer.

Name: PillowLayer.

Upload pillow-layer.zip.

Runtime: Python 3.12

Create.

Go to your Lambda function → Layers → Add layer → Select PillowLayer.
--------------------------------------------------------------------------------------------

## Step 8 — Add S3 Trigger
In your Lambda function → Configuration → Triggers → Add trigger.

Select S3.

Bucket: my-original-images-bucket.

Event: PUT (Object Created).

Save.


✅ Now, whenever you upload a .jpg or .png to my-original-images-bucket,
Lambda will resize it to 200x200 and upload it to my-resized-images-bucket.

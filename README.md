# AWS Lambda Image Resizer

This is a **serverless image resizing application** built using AWS Lambda, S3, and Python.

## Features
- Automatically resizes images to 300x300 pixels when uploaded to S3.
- Uses AWS Lambda for serverless execution.
- Stores resized images in a separate destination bucket.

## Architecture
1. User uploads an image to **Source S3 Bucket**.
2. S3 triggers **AWS Lambda**.
3. Lambda uses **Pillow** to resize the image.
4. Resized image is stored in **Destination S3 Bucket**.

## Tech Stack
- AWS Lambda
- Amazon S3
- Python (Pillow, boto3)

## Setup
1. Create **Source** and **Destination** S3 buckets.
2. Deploy this Lambda function.
3. Configure S3 event trigger for `PUT` operations.
4. Upload an image and check the destination bucket.



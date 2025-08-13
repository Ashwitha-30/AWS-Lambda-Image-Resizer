# AWS Lambda S3 Image Resizer Setup Guide

## Step 1 — Create an S3 Bucket for Original Images
1. Open **AWS Console** → **S3**.
2. Click **Create bucket** → Name: `my-original-images-bucket`.
3. Region: choose same as Lambda will be in.
4. Leave other settings default → **Create bucket**.

---

## Step 2 — Create an S3 Bucket for Resized Images
1. Create another bucket: `my-resized-images-bucket`.
2. Keep default settings → **Create bucket**.

---

## Step 3 — Create IAM Role for Lambda
1. Go to **IAM** → **Roles** → **Create role**.
2. Select **AWS service** → **Lambda**.
3. Attach policies:
   - ✅ `AmazonS3FullAccess`
   - ✅ `CloudWatchLogsFullAccess`
4. Name it: `lambda-s3-fullaccess-role` → **Create role**.

---

## Step 4 — Prepare Python Code on Linux
On your Ubuntu/Linux terminal:
```bash
mkdir image-resizer
cd image-resizer
nano lambda_function.py
```

Paste this code (Python 3.x):
```python
import boto3
import os
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get bucket and file info
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download image from S3
    download_path = f"/tmp/{os.path.basename(key)}"
    s3.download_file(bucket_name, key, download_path)
    
    # Resize image
    resized_path = f"/tmp/resized-{os.path.basename(key)}"
    with Image.open(download_path) as img:
        img = img.resize((200, 200))
        img.save(resized_path)
    
    # Upload to resized bucket
    s3.upload_file(resized_path, 'my-resized-images-bucket', os.path.basename(resized_path))
    
    return {
        'statusCode': 200,
        'body': f"Image resized and uploaded as {resized_path}"
    }
```

Save & exit:
```bash
CTRL+O, ENTER, CTRL+X
```

---

## Step 5 — Install Pillow & Create Zip Files
```bash
mkdir python
pip install pillow -t python/
zip -r pillow-layer.zip python
zip function-code.zip lambda_function.py
```
You now have:
- `pillow-layer.zip` → Layer for image processing.
- `function-code.zip` → Your Lambda code.

---

## Step 6 — Create Lambda & Add Code
1. In AWS Console → **Lambda** → **Create function**.
2. Name: `image-resizer-func`.
3. Runtime: **Python 3.12**
4. Role: Choose existing → `lambda-s3-fullaccess-role`.
5. Create function.
6. In **Code** → Upload from `.zip` → Select `function-code.zip`.
7. **Deploy**.

---

## Step 7 — Add Pillow Layer
1. In **Lambda** → **Layers** → **Create layer**.
2. Name: `PillowLayer`.
3. Upload `pillow-layer.zip`.
4. Runtime: **Python 3.12**
5. Create.
6. Go to your Lambda function → **Layers** → **Add layer** → Select `PillowLayer`.

---

## Step 8 — Add S3 Trigger
1. In your Lambda function → **Configuration** → **Triggers** → **Add trigger**.
2. Select **S3**.
3. Bucket: `my-original-images-bucket`.
4. Event: **PUT (Object Created)**.
5. Save.

---

✅ **Now, whenever you upload a `.jpg` or `.png` to `my-original-images-bucket`, Lambda will resize it to 200x200 and upload it to `my-resized-images-bucket`.**

import json
import boto3
import os
import urllib.parse

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get S3 bucket and key from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response['Body'].read().decode('utf-8', errors='ignore')

        # Check for empty content
        if not content.strip():
            print("⚠️ Empty file. No data to process.")
            return {"statusCode": 400, "body": "Empty S3 file."}

        inserted = 0

        # Process each line as a JSON object
        for line in content.strip().splitlines():
            if not line:
                continue
            try:
                item = json.loads(line)

                # Skip if sensorId is missing
                if 'sensorId' not in item:
                    print("⚠️ Skipping item without sensorId:", item)
                    continue

                # Convert sensorId to string if needed
                item['sensorId'] = str(item['sensorId'])

                # Insert into DynamoDB
                table.put_item(Item=item)
                inserted += 1

            except json.JSONDecodeError as e:
                print("Skipping invalid JSON line:", line)
                print("Error:", e)

        print(f"✅ Inserted {inserted} record(s) into DynamoDB.")
        return {"statusCode": 200, "body": f"Inserted {inserted} records"}

    except Exception as e:
        print("❌ Error:", e)
        return {"statusCode": 500, "body": str(e)}

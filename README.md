Step 1: Create Kinesis Data Stream
1.	Go to Kinesis > Data Streams
2.	Click Create data stream
3.	Example name: namrata-stream
4.	Choose the default settings and create
Step 2: Create Kinesis Firehose Delivery Stream
1.	Go to Kinesis > Delivery streams
2.	Click Create delivery stream
3.	Choose:
o	Source: Kinesis Data Stream
o	Destination: Amazon S3
4.	Set:
o	Source stream: namrata-stream
o	Destination bucket: megaproject-bin
5.	(Optional) Enable Dynamic Partitioning if using it, and configure with metadata extraction.
6.	Create the Firehose stream
Step 3: Use Kinesis Data Generator (KDG)
1.	Go to Kinesis Data Generator
2.	Login via Cognito
Git hub link – for genereate cognito user :https://awslabs.github.io/amazon-kinesis-data-generator/web/help.html
 
Use this template as test data:
{
  "sensorId": "s128",
  "temperature": 78,
  "timestamp": "2025-05-25T16:25:00Z",
  "deviceType": "thermometer"
}

 
Next >>
 

Step 4: Create an S3 Bucket
1.	Go to S3 > Create bucket
2.	Example bucket name: megaproject-bin
3.	Uncheck "Block all public access" if needed for testing (not recommended for production)
4.	Create the bucket
 

Step 5: Create Lambda Function (S3 Trigger)
1.	Go to Lambda > Create function
2.	Runtime: Python 3.9
3.	Use inline or upload lambda_function.py (from this repo)
4.	Set Environment Variable:
o	DYNAMODB_TABLE = namratadb
5.	In Permissions, ensure Lambda's IAM role has:
o	s3:GetObject
o	dynamodb:PutItem
6.	Add a trigger:
o	Source: S3
o	Bucket: megaproject-bin
o	Event: PUT (Object created)


 


Step 6: Set Up DynamoDB Table
1.	Go to the AWS Console > DynamoDB.
2.	Create a new table:
o	Table name: namratadb (or your preferred name)
o	Partition key: sensorId
o	Type: String
3.	Leave all other settings as default and create the table.
Step 7: Test the Full Flow
1.	Send sample data from the Kinesis Data Generator
2.	Wait for the Firehose to deliver to S3
3.	Lambda will trigger and insert data into DynamoDB
Check logs in CloudWatch and records in DynamoDB to confirm.


 


 




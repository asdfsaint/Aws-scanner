import boto3
from botocore.exceptions import ClientError, NoCredentialsError

session = boto3.Session()
sts = session.client("sts")
s3 = session.client("s3")

try:
    identity = sts.get_caller_identity()
    print(f"Connected as: {identity['Arn']}")
    print(f"Account ID:  {identity['Account']}")
except NoCredentialsError:
    print("No credentials found. Run 'aws configure' first.")
except ClientError as e:
    print(f"AWS rejected the request: {e}")

try:
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])
except ClientError as e:
    print (f"Failed to list buckets: {e}")




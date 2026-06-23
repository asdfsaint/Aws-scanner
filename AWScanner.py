import boto3
from botocore.exceptions import ClientError, NoCredentialsError

session = boto3.Session()
sts = session.client("sts")

try:
    identity = sts.get_caller_identity()
    print(f"Connected as: {identity['Arn']}")
    print(f"Account ID:  {identity['Account']}")
except NoCredentialsError:
    print("No credentials found. Run 'aws configure' first.")
except ClientError as e:
    print(f"AWS rejected the request: {e}")
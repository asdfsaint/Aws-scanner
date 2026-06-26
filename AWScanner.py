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

    public_access = s3.get_public_access_block(Bucket=bucket['Name'])
    if public_access['PublicAccessBlockConfiguration']['BlockPublicAcls']:
        print (f"PASS: {bucket['Name']} BlockPublicAcls is enabled")
    else:
        print (f"FAIL: {bucket['Name']} BlockPublicAcls is disabled")
    
    if public_access['PublicAccessBlockConfiguration']['IgnorePublicAcls']:
        print(f"PASS: {bucket['Name']} IgnorePublicAcls is enabled")
    
    else:
        print (f"FAIL:{bucket['Name']} IgnorePublicAcls is disabled")

    if public_access['PublicAccessBlockConfiguration']['BlockPublicPolicy']:
        print(f"PASS: {bucket['Name']} BlockPublicPolicy is enabled")
    
    else:
        print (f"FAIL: {bucket['Name']} BlockPublicPolicy is disabled")

    if public_access['PublicAccessBlockConfiguration']['RestrictPublicBuckets']:
        print (f"PASS: {bucket['Name']} RestrictPublicBuckets is enabled")
    
    else:
        print (f"FAIL: {bucket['Name']} RestrictPublicBuckets is disabled")


    try:
        encryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
        algorithm = encryption['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
        if algorithm:
            print (f"PASS: {bucket['Name']} Encryption Enabled with {algorithm}")
    except ClientError as e:
        if e.response ['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFound':
            print (f"FAIL: {bucket['Name']} Encryption Disabled {e.response['Error']['Code']}")    


except ClientError as e:
    print (f"Failed to list buckets: {e}")  
    
    




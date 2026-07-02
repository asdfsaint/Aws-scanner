import boto3
from botocore.exceptions import ClientError, NoCredentialsError

session = boto3.Session()
sts = session.client("sts")
s3 = session.client("s3")
iam = session.client("iam")

#Confirming AWS credentials are valid before running any security checks
try:
    identity = sts.get_caller_identity()
    print(f"Connected as: {identity['Arn']}")
    print(f"Account ID:  {identity['Account']}")
except NoCredentialsError:
    print("No credentials found. Run 'aws configure' first.")
except ClientError as e:
    print(f"AWS rejected the request: {e}")


#List all AWS buckets on account so the checks below it can run against every single bucket
try:
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        print(bucket['Name'])

    #Confirms IAM public-access-block settings block public ACLs and policies at the bucket level
    try:
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

    except ClientError as e:
        if e.response ['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            print (f"FAIL: {bucket['Name']} NoPublicaccess {e.response ['Error']['Code']}")
        
        else:
            print (f"FAIL: {bucket['Name']} {e.response ['Error']['Code']}")
    
            

    
    
    
#Checks for default server side encryption on buckets and encryption type
    try:
        encryption = s3.get_bucket_encryption(Bucket=bucket['Name'])
        algorithm = encryption['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']['SSEAlgorithm']
        print (f"PASS: {bucket['Name']} Encryption Enabled with {algorithm}")
    except ClientError as e:
        if e.response ['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFound':
            print (f"FAIL: {bucket['Name']} Encryption Disabled {e.response['Error']['Code']}")    
        else:
            print (f"FAIL: {bucket['Name']} {e.response['Error']['Code']}")

except ClientError as e:
    print (f"Failed to list buckets: {e}")  


# Gets account summary and checks for root access keys and if MFA is enabled
try:
    summary = iam.get_account_summary()
    print (f"User summary: {summary['SummaryMap'] ['Users']}")
    print (f"Amount of MFADevices: {summary['SummaryMap'] ['MFADevices']}")

    
    if summary['SummaryMap']['AccountMFAEnabled'] == 0:
        print (f"FAIL: Enable Multi Factor Authentication")
    else:
        print (f"PASS: Multi factor Authentication Enabled")

    if summary['SummaryMap']['AccountAccessKeysPresent'] == 1:
        print (f"FAIL: Remove Root access keys")
    else:
        print (f"PASS: No Root access keys")

except ClientError as e:
    if e.response ['Error']['Code'] == 'ServiceFailure':
        print(f"FAIL:Failed to get account summary {e.response ['Error'] ['Code']}")
    else:
        print(f"FAIL: {e.response ['Error'] ['Code']}")





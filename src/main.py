import os
import boto3

def get_s3_resource():
    
    role_arn = os.environ.get("AWS_CROSS_ACCOUNT_ROLE_ARN")
    bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
    
    if not role_arn or not bucket_name:
        raise ValueError("Missing required environment variables.")


    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="ReproduciblePublicSession"
    )
    creds = assumed_role['Credentials']

    return boto3.resource(
        's3',
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken'],
    )

def get_ec2_resource():
    
    role_arn = os.environ.get("AWS_CROSS_ACCOUNT_ROLE_ARN")
    bucket_name = os.environ.get("AWS_EC2_INSTANCE_NAME")
    
    if not role_arn or not bucket_name:
        raise ValueError("Missing required environment variables.")

    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName="ReproduciblePublicSession"
    )
    creds = assumed_role['Credentials']

    return boto3.resource(
        'ec2',
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken'],
    )

def s3_resource_monitor():
    s2_resource = get_s3_resource()
    pass


def ec2_resoure_monitor():
    ec2_resource = get_ec2_resource()
    pass



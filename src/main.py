import os
import time
import datetime
import matplotlib as plt
import psutil
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, EndpointConnectionError

class AWSMonitorAgent:
    def __init__(self, role_arn: str, bucket_names: list, region_name: str = "us-east-1"):
        if not role_arn or not bucket_names:
            raise ValueError("Missing required variables: role_arn or bucket_names.")
            
        self.role_arn = role_arn
        self.bucket_names = bucket_names
        self.region_name = region_name
        self.start_time = time.time()

        self.sts_client = boto3.client("sts", region_name=self.region_name)
        self.s3_client = boto3.client('s3', **self._get_credentials_dict())
        self.s3_client.create_bucket(f"{self._get_credentials_dict()}'s Bucket")
        
        try:
            self.assumed_role = self.sts_client.assume_role(
                RoleArn=self.role_arn,
                RoleSessionName="MonitorSession",
            )
            self.creds = self.assumed_role["Credentials"]
            print("Successfully assumed monitoring IAM role.")
        except Exception as e:
            print(f"Failed to assume IAM role: {e}")
            raise

    def _get_credentials_dict(self):
        """Helper to pass assumed role tokens to clients/resources."""
        return {
            "aws_access_key_id": self.creds["AccessKeyId"],
            "aws_secret_access_key": self.creds["SecretAccessKey"],
            "aws_session_token": self.creds["SessionToken"],
            "region_name": self.region_name
        }

    def _get_live_metrics(self):
        """Dynamically calculates current system utilization and latency."""
        return {
            "I/O latency": time.time() - self.start_time,
            "CPU_usage": psutil.cpu_percent(interval=0.1), 
            "RAM_usage": psutil.virtual_memory().percent,
            "Datetime": datetime.datetime.now().isoformat()
        }
    
    def __log_to_bucket(self, ec2=False, braket=False):
        """Logs the associated data to S3."""
        if (ec2 == True):
            self.s3_client.put_object(body=self.get_ec2_resource)
        elif (braket == True):
            self.s3_client.put_object(body=self.get_ec2_resource)

    def __generate_viz(self):
        # From bucket, obtain 5 records over a period, and auto generate a viz from matpltlib
        git_link = "https://github.com/ajlrza/aws_benchmark_q-algorithms.git"
        list_objects = self.s3.list_objects_v2(
            Bucket=f"{self._get_credentials_dict()}'s Bucket",
            MaxKeys=5
        )

        if 'Contents' in response:
         for obj in response['Contents']:
             get_object = self.s3.get_object(
                 Bucket=f"{self._get_credentials_dict()}'s Bucket",
                 Key=obj['Key']
             )

    def get_s3_resource(self):
        try:
            # Use assumed credentials to create client
            s3_client = boto3.client('s3', **self._get_credentials_dict())
            s3_client.list_buckets() 
            print("S3 tracking successful.")
            
            s3_resource = boto3.resource('s3', **self._get_credentials_dict())
            return {
                "infrastructure_metrics": {
                    "S3_resource": s3_resource,
                    **self._get_live_metrics()
                }
            }
        except (NoCredentialsError, ClientError, EndpointConnectionError) as e:
            print(f"S3 Monitoring Error: {e}")
            return None

    def get_ec2_resource(self):
        try:
            ec2_client = boto3.client('ec2', **self._get_credentials_dict())
            ec2_client.describe_instances() 
            print("EC2 tracking successful.")

            ec2_resource = boto3.resource('ec2', **self._get_credentials_dict())
            return {
                "infrastructure_metrics": {
                    "EC2_resource": ec2_resource,
                    **self._get_live_metrics()
                }
            }
        except (NoCredentialsError, ClientError, EndpointConnectionError) as e:
            print(f"EC2 Monitoring Error: {e}")
            return None
    
    def get_braket_metrics(self):
        try:
            braket_client = boto3.client('braket', **self._get_credentials_dict())
            braket_client.search_devices(filters=[]) 
            print("Braket tracking successful.")

            return {
                "infrastructure_metrics": {
                    "Braket_client": braket_client, 
                    **self._get_live_metrics()
                }
            }
        except (NoCredentialsError, ClientError, EndpointConnectionError) as e:
            print(f"Braket Monitoring Error: {e}")
            return None

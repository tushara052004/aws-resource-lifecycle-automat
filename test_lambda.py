import os
import boto3
from moto import mock_aws

os.environ["AWS_ACCESS_KEY_ID"] = "fake"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

from awsLambda import lambda_handler

with mock_aws():
    ec2_us = boto3.client("ec2", region_name="us-east-1")
    ec2_eu = boto3.client("ec2", region_name="eu-west-1")
    rds_us = boto3.client("rds", region_name="us-east-1")

    ec2_us.run_instances(ImageId="ami-12345678", MinCount=1, MaxCount=1)
    ec2_eu.run_instances(
        ImageId="ami-12345678", MinCount=1, MaxCount=1,
        TagSpecifications=[{
            "ResourceType": "instance",
            "Tags": [{"Key": "user", "Value": "tushara"}],
        }],
    )
    rds_us.create_db_instance(
        DBInstanceIdentifier="db-no-tags",
        DBInstanceClass="db.t3.micro",
        Engine="mysql",
        MasterUsername="admin",
        MasterUserPassword="password123",
        AllocatedStorage=20,
    )

    print("\n=== Running the Lambda ===")
    result = lambda_handler({}, None)

    print("\n=== RESULTS ===")
    print("Lambda returned:", result)
    for label, client in [("EC2 us-east-1, no tags", ec2_us),
                          ("EC2 eu-west-1, user tag", ec2_eu)]:
        for res in client.describe_instances()["Reservations"]:
            for i in res["Instances"]:
                print(label, "->", i["State"]["Name"])
    for db in rds_us.describe_db_instances()["DBInstances"]:
        print("RDS us-east-1, no tags ->", db["DBInstanceStatus"])
import os
import boto3
from moto import mock_aws

os.environ["AWS_ACCESS_KEY_ID"] = "fake"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

from rds import Rds


def make(rds, name, tags):
    rds.create_db_instance(
        DBInstanceIdentifier=name,
        DBInstanceClass="db.t3.micro",
        Engine="mysql",
        MasterUsername="admin",
        MasterUserPassword="password123",
        AllocatedStorage=20,
        Tags=[{"Key": k, "Value": v} for k, v in tags.items()],
    )


def show(rds):
    for db in rds.describe_db_instances()["DBInstances"]:
        print("   ", db["DBInstanceIdentifier"], "->", db["DBInstanceStatus"])


with mock_aws():
    rds = boto3.client("rds", region_name="us-east-1")
    make(rds, "db-a-has-user-tag", {"user": "tushara"})
    make(rds, "db-b-no-tags", {})
    make(rds, "db-c-excludepower", {"excludepower": "true"})

    print("\nBEFORE:")
    show(rds)

    Rds("us-east-1").cleanup_instances()

    print("\nAFTER:")
    show(rds)
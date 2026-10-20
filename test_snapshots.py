import os
import boto3
from moto import mock_aws

os.environ["AWS_ACCESS_KEY_ID"] = "fake"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

from ec2 import Ec2Instances

with mock_aws():
    ec2 = boto3.client("ec2", region_name="us-east-1")
    vol = ec2.create_volume(AvailabilityZone="us-east-1a", Size=1)
    ec2.create_snapshot(VolumeId=vol["VolumeId"])
    ec2.create_snapshot(VolumeId=vol["VolumeId"])

    tool = Ec2Instances("us-east-1")
    found = tool.get_user_created_snapshots()["Snapshots"]
    print("\nSnapshots the script can see:", len(found))

    deleted = tool.delete_snapshots(0)
    print("Snapshots deleted:", deleted)

    left = tool.get_user_created_snapshots()["Snapshots"]
    print("Snapshots left:", len(left))
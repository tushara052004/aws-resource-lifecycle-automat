import os
import boto3
from moto import mock_aws

# Fake keys. They only work with the pretend AWS.
os.environ["AWS_ACCESS_KEY_ID"] = "fake"
os.environ["AWS_SECRET_ACCESS_KEY"] = "fake"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

from ec2 import Ec2Instances


def launch(ec2, tags):
    kwargs = {}
    if tags:
        tag_list = [{"Key": k, "Value": v} for k, v in tags.items()]
        kwargs["TagSpecifications"] = [
            {"ResourceType": "instance", "Tags": tag_list}
        ]
    r = ec2.run_instances(ImageId="ami-12345678", MinCount=1, MaxCount=1, **kwargs)
    return r["Instances"][0]["InstanceId"]


def show(ec2, names):
    for res in ec2.describe_instances()["Reservations"]:
        for i in res["Instances"]:
            print("   ", names[i["InstanceId"]], "->", i["State"]["Name"])


with mock_aws():
    ec2 = boto3.client("ec2", region_name="us-east-1")
    names = {}
    names[launch(ec2, {"user": "tushara"})] = "A: has user tag"
    names[launch(ec2, {})] = "B: no tags at all"
    names[launch(ec2, {"user": "x", "excludepower": "true"})] = "C: user + excludepower"
    names[launch(ec2, {"Name": "test"})] = "D: tag but no user tag"
    ec2.create_volume(AvailabilityZone="us-east-1a", Size=1)

    print("\nBEFORE:")
    show(ec2, names)
    print("Volumes before:", len(ec2.describe_volumes()["Volumes"]))

    tool = Ec2Instances("us-east-1")
    tool.shutdown()
    tool.delete_available_volumes()

    print("\nAFTER:")
    show(ec2, names)
    print("Volumes after:", len(ec2.describe_volumes()["Volumes"]))
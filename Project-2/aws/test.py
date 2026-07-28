from aws.auth import AWSAuth
from aws.client_factory import AWSClientFactory

auth = AWSAuth(
    profile_name="default",
    region_name="ap-south-1"
)

factory = AWSClientFactory(auth)

ec2 = factory.get_client("ec2")

print(ec2)
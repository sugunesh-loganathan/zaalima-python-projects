from aws.auth import AWSAuth
from aws.client_factory import AWSClientFactory
from aws.ec2 import EC2Service


auth = AWSAuth(
    profile_name="default",
    region_name="ap-south-1"
)

factory = AWSClientFactory(auth)

ec2 = EC2Service(factory)

instances = ec2.list_instances()

for instance in instances:
    print(instance)
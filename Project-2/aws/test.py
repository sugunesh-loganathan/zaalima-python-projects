from aws.auth import AWSAuth
from aws.client_factory import AWSClientFactory

auth = AWSAuth()

factory = AWSClientFactory(auth)

ec2 = factory.get_client("ec2")
cloudwatch = factory.get_client("cloudwatch")

sts = factory.get_client("sts")


print(ec2)
print(cloudwatch)
print(sts)
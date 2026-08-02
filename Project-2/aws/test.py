#EC2 SERVICE


# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.ec2 import EC2Service


# auth = AWSAuth(
#     profile_name="default",
#     region_name="ap-south-1"
# )

# factory = AWSClientFactory(auth)

# ec2 = EC2Service(factory)

# instances = ec2.list_instances()

# for instance in instances:
#     print(instance)


#EBS SERVICE

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.ebs import EBSService

# auth = AWSAuth(
#     profile_name="default",
#     region_name="ap-south-1"
# )

# factory = AWSClientFactory(auth)
# ebs = EBSService(factory)

# # API sirf ek baar call hogi
# volumes = ebs.list_volumes()

# if not volumes:
#     print("No EBS volumes found.")
# else:
#     print(f"Total Volumes: {len(volumes)}")
#     for volume in volumes:
#         print(volume)

# print("\nUnattached Volumes:")

# # Pehle se fetched data pass kar rahe hain
# unused = ebs.get_unattached_volumes(volumes)

# if not unused:
#     print("No unattached volumes found.")
# else:
#     for volume in unused:
#         print(volume)

#EIP(ELASTIC IP)

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.eip import ElasticIPService

# auth = AWSAuth(
#     profile_name="default",
#     region_name="ap-south-1"
# )

# factory = AWSClientFactory(auth)

# eip = ElasticIPService(factory)

# addresses = eip.list_addresses()

# if not addresses:
#     print("No Elastic IPs found.")
# else:
#     print(f"Total Elastic IPs: {len(addresses)}")
#     for address in addresses:
#         print(address)

# print("\nUnassociated Elastic IPs:")

# unused = eip.get_unassociated_addresses(addresses)

# if not unused:
#     print("No unassociated Elastic IPs found.")
# else:
#     for address in unused:
#         print(address)

# CLUDWATCH
from aws.auth import AWSAuth
from aws.client_factory import AWSClientFactory
from aws.cloudwatch import CloudWatchService
from aws.ec2 import EC2Service

auth = AWSAuth(
    profile_name="default",
    region_name="ap-south-1"
)

factory = AWSClientFactory(auth)

ec2 = EC2Service(factory)

instances = ec2.list_instances()

if not instances:
    print("No EC2 instances found.")
else:

    cloudwatch = CloudWatchService(factory)

    for instance in instances:

        cpu = cloudwatch.get_average_cpu(
            instance["InstanceId"]
        )

        print(instance["InstanceId"], cpu)
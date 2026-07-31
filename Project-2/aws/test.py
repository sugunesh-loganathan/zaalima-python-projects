from aws.auth import AWSAuth
from aws.client_factory import AWSClientFactory
from aws.ebs import EBSService

auth = AWSAuth(
    profile_name="default",
    region_name="ap-south-1"
)

factory = AWSClientFactory(auth)
ebs = EBSService(factory)

# API sirf ek baar call hogi
volumes = ebs.list_volumes()

if not volumes:
    print("No EBS volumes found.")
else:
    print(f"Total Volumes: {len(volumes)}")
    for volume in volumes:
        print(volume)

print("\nUnattached Volumes:")

# Pehle se fetched data pass kar rahe hain
unused = ebs.get_unattached_volumes(volumes)

if not unused:
    print("No unattached volumes found.")
else:
    for volume in unused:
        print(volume)
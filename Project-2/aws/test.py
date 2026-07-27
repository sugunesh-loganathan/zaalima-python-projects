from aws.auth import AWSAuth

auth = AWSAuth(
    profile_name="default",
    region_name="ap-south-1"
)

session = auth.create_session()
print(session)

identity = auth.validate_credentials()

print(identity)
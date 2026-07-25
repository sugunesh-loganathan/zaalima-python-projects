from aws.auth import AWSAuth

auth = AWSAuth(region_name="ap-south-1")

session = auth.create_session()

print(session)
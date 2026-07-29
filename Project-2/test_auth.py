from app.aws.auth import AWSAuthenticator

auth = AWSAuthenticator()

session = auth.authenticate()

print(session)
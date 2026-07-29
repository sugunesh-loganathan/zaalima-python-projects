from .session import AWSSession

class AWSAuthenticator:
    
    def __init__(self):
        self.session = AWSSession()

    def authenticate(self):
        return self.session.create_session()
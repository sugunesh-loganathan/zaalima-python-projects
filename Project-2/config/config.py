from config.regions import SUPPORTED_REGIONS, DEFAULT_REGION


class Config:

    def __init__(self, region=None):
        self.region = region or DEFAULT_REGION

    def get_region(self):
        return self.region

    def validate_region(self):

        if self.region not in SUPPORTED_REGIONS:
            raise ValueError(f"Unsupported AWS Region: {self.region}")

        return True
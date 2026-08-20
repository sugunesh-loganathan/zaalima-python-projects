class ScanResult:


    def __init__(
        self,
        service: str,
        status: str,
        resources_found: int,
        message: str,
    ):
        self.service = service
        self.status = status
        self.resources_found = resources_found
        self.message = message

    def to_dict(self):
        return {
            "service": self.service,
            "status": self.status,
            "resources_found": self.resources_found,
            "message": self.message,
        }
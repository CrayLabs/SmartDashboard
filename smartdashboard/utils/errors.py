class SSDashboardError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message


class ManifestError(SSDashboardError):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class MalformedManifestError(ManifestError):
    def __init__(self, message: str) -> None:
        super().__init__(message)

###THESE NEED WORK!!!!!
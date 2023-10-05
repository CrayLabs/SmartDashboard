class SSDashboardError(Exception):
    def __init__(self, title: str, file: str, exception: Exception) -> None:
        self.title = title
        self.file = file
        self.exception = exception


class ManifestError(SSDashboardError):
    def __init__(self, title: str, file: str, exception: Exception) -> None:
        modified_title = f"ManifestError: {title}"
        super().__init__(title, file, exception)
        self.title = modified_title


class MalformedManifestError(ManifestError):
    def __init__(self, title: str, file: str, exception: Exception) -> None:
        modified_title = f"MalformedManifestError: {title}"
        super().__init__(title, file, exception)
        self.title = modified_title

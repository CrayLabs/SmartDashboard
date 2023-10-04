class SSDashboardError(Exception):
    def __init__(self, title: str, file: str, body: Exception) -> None:
        self.title = title
        self.file = file
        self.body = body


class ManifestError(SSDashboardError):
    def __init__(self, title: str, file: str, body: Exception) -> None:
        modified_title = f"ManifestError: {title}"
        super().__init__(title, file, body)
        self.title = modified_title


class MalformedManifestError(ManifestError):
    def __init__(self, title: str, file: str, body: Exception) -> None:
        modified_title = f"MalformedManifestError: {title}"
        super().__init__(title, file, body)
        self.title = modified_title

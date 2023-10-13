class SSDashboardError(Exception):
    def __init__(self, title: str, file: str, exception: Exception) -> None:
        super().__init__(title)
        self.title = title
        self.file = file
        self.exception = exception

    def __str__(self) -> str:
        return f"{type(self).__name__}: {self.title}"


class ManifestError(SSDashboardError):
    ...


class MalformedManifestError(ManifestError):
    ...

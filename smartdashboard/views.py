import typing as t


class ExperimentView:
    def __init__(self) -> None:
        self.status: t.Optional[str] = None


class ApplicationView:
    def __init__(self) -> None:
        self.status: t.Optional[str] = None


class OrchestratorView:
    def __init__(self) -> None:
        self.status: t.Optional[str] = None


class EnsembleView:
    def __init__(self) -> None:
        self.status: t.Optional[str] = None

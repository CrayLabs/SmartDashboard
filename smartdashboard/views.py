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


class ErrorView:
    def __init__(self) -> None:
        self.status: t.Optional[str] = None


class OverviewView:
    def __init__(
        self,
        exp_view: ExperimentView,
        app_view: ApplicationView,
        orc_view: OrchestratorView,
        ens_view: EnsembleView,
    ) -> None:
        self.exp_view = exp_view
        self.app_view = app_view
        self.ens_view = ens_view
        self.orc_view = orc_view
        super().__init__()

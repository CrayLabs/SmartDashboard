import typing as t


class View:
    """View base class for shared behaviors"""
    def __init__(self) -> None:
        self.status: t.Optional[str] = None


class ExperimentView(View):
    ...


class ApplicationView(View):
    ...


class OrchestratorView(View):
    ...


class EnsembleView(View):
    ...


class ErrorView:
    ...


class OverviewView:
    def __init__(
        self, exp_view: View, app_view: View, orc_view: View, ens_view: View
    ) -> None:
        self.exp_view = exp_view
        self.app_view = app_view
        self.ens_view = ens_view
        self.orc_view = orc_view
        super().__init__()

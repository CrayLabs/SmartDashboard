import typing as t

from streamlit.delta_generator import DeltaGenerator

from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.LogReader import get_logs


class ViewBase:
    ...


class EntityView(ViewBase):
    def __init__(self, view_model: t.Optional[t.Dict[str, t.Any]]) -> None:
        self.status: str = ""
        self.view_model = view_model
        self.out_logs_element = DeltaGenerator()
        self.err_logs_element = DeltaGenerator()

    @property
    def err_logs(self) -> str:
        return get_logs(file=get_value("err_file", self.view_model))

    @property
    def out_logs(self) -> str:
        return get_logs(file=get_value("out_file", self.view_model))

    def update(self) -> None:
        self.out_logs_element.code(self.out_logs)
        self.err_logs_element.code(self.err_logs)


class ExperimentView(EntityView):
    ...


class ApplicationView(EntityView):
    ...


class OrchestratorView(EntityView):
    ...


class EnsembleView(EntityView):
    ...


class ErrorView(ViewBase):
    ...


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

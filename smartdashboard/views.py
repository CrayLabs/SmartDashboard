import typing as t

from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.LogReader import get_logs

if t.TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


class ViewBase:
    ...


class EntityView(ViewBase):
    def __init__(self, view_model: t.Optional[t.Dict[str, t.Any]]) -> None:
        self.status: str = ""
        self.err_logs: str = ""
        self.err_logs_element: DeltaGenerator
        self.out_logs: str = ""
        self.out_logs_element: DeltaGenerator
        self.view_model = view_model

    def update(self) -> None:
        self.out_logs = get_logs(file=get_value("out_file", self.view_model))
        self.err_logs = get_logs(file=get_value("err_file", self.view_model))
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


class ErrorView(ViewBase):
    ...

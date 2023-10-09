import typing as t

from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.LogReader import get_logs

if t.TYPE_CHECKING:
    from streamlit.delta_generator import DeltaGenerator


class ViewBase(t.Protocol):
    def update(self) -> None:
        ...


class ExperimentView(ViewBase):
    def __init__(self) -> None:
        self.status: t.Optional[str] = None


class ApplicationView(ViewBase):
    def __init__(self) -> None:
        self.selected_application: t.Optional[t.Dict[str, t.Any]] = None
        self.status: t.Optional[str] = None
        self.err_logs: str = ""
        self.err_logs_element: t.Optional[DeltaGenerator] = None
        self.out_logs: str = ""
        self.out_logs_element: t.Optional[DeltaGenerator] = None

    def update(self) -> None:
        self.out_logs = get_logs(file=get_value("out_file", self.selected_application))
        self.err_logs = get_logs(file=get_value("err_file", self.selected_application))
        self.out_logs_element.code(self.out_logs)
        self.err_logs_element.code(self.err_logs)


class OrchestratorView(ViewBase):
    def __init__(self) -> None:
        self.selected_orchestrator: t.Optional[t.Dict[str, t.Any]] = None
        self.selected_shard: t.Optional[t.Dict[str, t.Any]] = None
        self.status: t.Optional[str] = None
        self.err_logs: str = ""
        self.err_logs_element: t.Optional[DeltaGenerator] = None
        self.out_logs: str = ""
        self.out_logs_element: t.Optional[DeltaGenerator] = None

    def update(self) -> None:
        self.out_logs = get_logs(file=get_value("out_file", self.selected_shard))
        self.err_logs = get_logs(file=get_value("err_file", self.selected_shard))
        self.out_logs_element.code(self.out_logs)
        self.err_logs_element.code(self.err_logs)


class EnsembleView(ViewBase):
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


class ErrorView(ViewBase):
    def __init__(self) -> None:
        self.status: t.Optional[str] = None

import typing as t

from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.LogReader import get_logs

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
        self.out_logs_element.code(self.out_logs, language=None)
        self.err_logs_element.code(self.err_logs, language=None)


class ExperimentView(ViewBase):
    ...

    def update(self) -> None:
        self.out_logs = get_logs(file=get_value("out_file", self.view_model))
        self.err_logs = get_logs(file=get_value("err_file", self.view_model))
        self.out_logs_element.code(self.out_logs)
        self.err_logs_element.code(self.err_logs)


class ApplicationView(EntityView):
    ...

    def update(self) -> None:
        self.out_logs = get_logs(file=get_value("out_file", self.selected_application))
        self.err_logs = get_logs(file=get_value("err_file", self.selected_application))
        self.out_logs_element.code(self.out_logs)
        self.err_logs_element.code(self.err_logs)

class OrchestratorView(EntityView):
    ...


class EnsembleView(EntityView):
    ...


class ErrorView(ViewBase):
    ...


class OverviewView:
    def __init__(
        self,
        app_view: ApplicationView,
        orc_view: OrchestratorView,
        ens_view: EnsembleView,
    ) -> None:
        self.app_view = app_view
        self.ens_view = ens_view
        self.orc_view = orc_view


class ErrorView(ViewBase):
    ...

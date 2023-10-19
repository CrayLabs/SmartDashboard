import typing as t

from streamlit.delta_generator import DeltaGenerator

from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.LogReader import get_logs
from smartdashboard.utils.StatusReader import (
    format_status,
    get_ensemble_status_summary,
    get_experiment_status_summary,
    get_orchestrator_status_summary,
    get_status,
)

from streamlit.delta_generator import DeltaGenerator

from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.LogReader import get_logs



class ViewBase:
    def update(self) -> None:
        pass


class EntityView(ViewBase):
    def __init__(self, view_model: t.Optional[t.Dict[str, t.Any]]) -> None:
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
        self.update_logs()
        self.update_status()

    def update_logs(self) -> None:
        self.out_logs_element.code(self.out_logs)
        self.err_logs_element.code(self.err_logs)

    def update_status(self) -> None:
        pass


class ExperimentView(ViewBase):
    def __init__(self, experiment: t.Optional[t.Dict[str, t.Any]]) -> None:
        self.status: str = ""
        self.status_element = DeltaGenerator()
        self.experiment = experiment
        self.runs: t.List[t.Dict[str, t.Any]] = []

    def update(self) -> None:
        self.status = get_experiment_status_summary(self.runs)
        self.status_element.write(self.status)

    def update(self) -> None:
        self.out_logs_element.code(self.out_logs)
        self.err_logs_element.code(self.err_logs)


class ApplicationView(EntityView):
    def __init__(self, application: t.Optional[t.Dict[str, t.Any]]) -> None:
        self.status: str = ""
        self.status_element = DeltaGenerator()
        self.application = application
        super().__init__(view_model=application)

    def update_status(self) -> None:
        if self.application is not None:
            self.status = format_status(
                get_status(self.application["telemetry_metadata"]["status_dir"])
            )
        else:
            self.status = "Status: "
        self.status_element.write(self.status)

    def update(self) -> None:
        self.out_logs = get_logs(file=get_value("out_file", self.selected_application))
        self.err_logs = get_logs(file=get_value("err_file", self.selected_application))
        self.out_logs_element.code(self.out_logs)
        self.err_logs_element.code(self.err_logs)

class OrchestratorView(EntityView):
    def __init__(
        self,
        orchestrator: t.Optional[t.Dict[str, t.Any]],
        shard: t.Optional[t.Dict[str, t.Any]],
    ) -> None:
        self.status: str = ""
        self.status_element = DeltaGenerator()
        self.orchestrator = orchestrator
        self.shard = shard
        super().__init__(view_model=shard)

    def update_status(self) -> None:
        self.status = get_orchestrator_status_summary(self.orchestrator)
        self.status_element.write(self.status)


class EnsembleView(EntityView):
    def __init__(
        self,
        ensemble: t.Optional[t.Dict[str, t.Any]],
        member: t.Optional[t.Dict[str, t.Any]],
    ) -> None:
        self.ensemble = ensemble
        self.member = member
        self.status: str = ""
        self.status_element = DeltaGenerator()
        self.member_status: str = ""
        self.member_status_element = DeltaGenerator()
        super().__init__(view_model=member)

    def update_status(self) -> None:
        self.status = get_ensemble_status_summary(self.ensemble)
        if self.member is not None:
            self.member_status = format_status(
                get_status(self.member["telemetry_metadata"]["status_dir"])
            )
        else:
            self.member_status = "Status: "
        self.status_element.write(self.status)
        self.member_status_element.write(self.member_status)


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

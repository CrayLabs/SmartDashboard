# BSD 2-Clause License
#
# Copyright (c) 2021-2024, Hewlett Packard Enterprise
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import typing as t
from abc import ABC, abstractmethod

from streamlit.delta_generator import DeltaGenerator

from smartdashboard.schemas.application import Application
from smartdashboard.schemas.base import HasOutErrFiles
from smartdashboard.schemas.ensemble import Ensemble
from smartdashboard.schemas.experiment import Experiment
from smartdashboard.schemas.orchestrator import Orchestrator
from smartdashboard.schemas.run import Run
from smartdashboard.schemas.shard import Shard
from smartdashboard.utils.LogReader import get_logs
from smartdashboard.utils.status import StatusEnum
from smartdashboard.utils.StatusReader import (
    StatusData,
    format_status,
    get_ensemble_status_summary,
    get_experiment_status_summary,
    get_orchestrator_status_summary,
    get_status,
)

_T = t.TypeVar("_T", bound=HasOutErrFiles)


class ViewBase(ABC):
    """Base class for Views. Views are groupings of UI elements
    that are displayed in the dashboard and are a representation
    of a SmartSim entity.

    Views update on a timestep of the event loop that renders
    elements in the dashboard.
    """

    @abstractmethod
    def update(self) -> None:
        """Abstract method to update elements in a view"""


class EntityView(t.Generic[_T], ViewBase):
    """View class for entities. Entities include
    Applications, Orchestrators, Shards, Ensembles, and Members.

    EntityViews are a collection of UI elements and have logs and
    statuses that update.
    """

    def __init__(self, view_model: t.Optional[_T]) -> None:
        """Initialize an EntityView

        :param view_model: Selected entity view
        :type view_model: Optional[_T]
        """
        self.view_model = view_model
        self.out_logs_element = DeltaGenerator()
        self.err_logs_element = DeltaGenerator()

    @property
    def err_logs(self) -> str:
        """Get error logs from selected entity view

        :return: Error logs
        :rtype: str
        """
        return get_logs(
            file=self.view_model.err_file if self.view_model is not None else ""
        )

    @property
    def out_logs(self) -> str:
        """Get output logs from selected entity view

        :return: Output logs
        :rtype: str
        """
        return get_logs(
            file=self.view_model.out_file if self.view_model is not None else ""
        )

    def update(self) -> None:
        """Update logs and status elements in the selected entity view"""
        self.update_logs()
        self._update_status()

    def update_logs(self) -> None:
        """Update error and output log elements in the selected entity view"""
        self.out_logs_element.code(self.out_logs, language="log")
        self.err_logs_element.code(self.err_logs, language="log")

    @abstractmethod
    def _update_status(self) -> None:
        """Abstract method to update an entity's status"""

    def update_view_model(self, new_view_model: t.Optional[_T]) -> None:
        """Update view_model

        This is called after a new entity is selected
        in the dashboard to keep displayed data in sync.

        :param new_view_model: Selected entity view
        :type new_view_model: Optional[_T]
        """
        if new_view_model is not None:
            self.view_model = new_view_model


class ExperimentView(EntityView[Experiment]):
    """View class for experiments"""

    def __init__(
        self,
        experiment: t.Optional[Experiment],
        runs: t.List[Run],
    ) -> None:
        """Initialize an ExperimentView

        :param experiment: The experiment to display
        :type experiment: Optional[Experiment]
        :param runs: Runs within an experiment
        :type runs: List[Run]
        """
        self.status_element = DeltaGenerator()
        self.runs = runs
        super().__init__(view_model=experiment)

    @property
    def status(self) -> str:
        """Get experiment status

        :return: Experiment status
        :rtype: str
        """
        return get_experiment_status_summary(self.runs)

    def _update_status(self) -> None:
        """Update status element in ExperimentView"""
        self.status_element.write(self.status)


class ApplicationView(EntityView[Application]):
    """View class for applications"""

    def __init__(self, application: t.Optional[Application]) -> None:
        """Initialize an ApplicationView

        :param application: Selected application to display
        :type application: Optional[Application]
        """
        self.status_element = DeltaGenerator()
        super().__init__(view_model=application)

    @property
    def application(self) -> t.Optional[Application]:
        """Get application associated with the view model

        :return: Selected application
        :rtype: Optional[Application]
        """
        return self.view_model

    @property
    def status(self) -> str:
        """Get application status

        :return: Status
        :rtype: str
        """
        if self.application is not None:
            try:
                status = get_status(self.application.telemetry_metadata["status_dir"])
            except KeyError:
                status = StatusData(StatusEnum.MALFORMED, None)
            return format_status(status)
        return "Status: "

    def _update_status(self) -> None:
        """Update status element in ApplicationView"""
        self.status_element.write(self.status)


class OrchestratorView(EntityView[Shard]):
    """View class for orchestrators"""

    def __init__(
        self,
        orchestrator: t.Optional[Orchestrator],
        shard: t.Optional[Shard],
    ) -> None:
        """Initialize an OrchestratorView

        :param orchestrator: Selected orchestrator to display
        :type orchestrator: Optional[Orchestrator]
        :param shard: Selected shard within the selected orchestrator
        :type shard: Optional[Shard]
        """
        self.orchestrator = orchestrator
        self.status_element = DeltaGenerator()
        super().__init__(view_model=shard)

    @property
    def shard(self) -> t.Optional[Shard]:
        """Get shard associated with the view model

        :return: Selected shard
        :rtype: Optional[Shard]
        """
        return self.view_model

    @property
    def status(self) -> str:
        """Get orchestrator status summary

        :return: Status summary
        :rtype: str
        """
        return get_orchestrator_status_summary(self.orchestrator)

    def _update_status(self) -> None:
        """Update status element in OrchestratorView"""
        self.status_element.write(self.status)


class EnsembleView(EntityView[Application]):
    """View class for ensembles"""

    def __init__(
        self,
        ensemble: t.Optional[Ensemble],
        member: t.Optional[Application],
    ) -> None:
        """Initialize an EnsembleView

        :param ensemble: Selected ensemble to display
        :type ensemble: Optional[Ensemble]
        :param member: Selected member to display
        :type member: Optional[Application]
        """
        self.ensemble = ensemble
        self.status_element = DeltaGenerator()
        self.member_status_element = DeltaGenerator()
        super().__init__(view_model=member)

    @property
    def member(self) -> t.Optional[Application]:
        """Get member associated with the view model

        :return: Selected member
        :rtype: Optional[Application]
        """
        return self.view_model

    @property
    def status(self) -> str:
        """Get ensemble status summary

        :return: Status summary
        :rtype: str
        """
        return get_ensemble_status_summary(self.ensemble)

    @property
    def member_status(self) -> str:
        """Get member status

        :return: Status
        :rtype: str
        """
        if self.member is not None:
            try:
                status = get_status(self.member.telemetry_metadata["status_dir"])
            except KeyError:
                status = StatusData(StatusEnum.MALFORMED, None)
            return format_status(status)
        return "Status: "

    def _update_status(self) -> None:
        """Update ensemble and member status elements in EnsembleView"""
        self.status_element.write(self.status)
        self.member_status_element.write(self.member_status)


class ErrorView(ViewBase):
    """View class for errors

    Contains UI elements for static display of unexpected exception
    information.
    """

    def update(self) -> None: ...


class OverviewView:
    """View class for the collection of views"""

    def __init__(
        self,
        exp_view: ExperimentView,
        app_view: ApplicationView,
        orc_view: OrchestratorView,
        ens_view: EnsembleView,
    ) -> None:
        """Initialize an OverviewView

        :param exp_view: Experiment view rendered in the dashboard
        :type exp_view: ExperimentView
        :param app_view: Application view rendered in the dashboard
        :type app_view: ApplicationView
        :param orc_view: Orchestrator view rendered in the dashboard
        :type orc_view: OrchestratorView
        :param ens_view: Ensemble view rendered in the dashboard
        :type ens_view: EnsembleView
        """
        self.exp_view = exp_view
        self.app_view = app_view
        self.ens_view = ens_view
        self.orc_view = orc_view

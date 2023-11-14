# BSD 2-Clause License
#
# Copyright (c) 2021-2023, Hewlett Packard Enterprise
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

from smartdashboard.utils.helpers import get_value
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


class ViewBase(ABC):
    """Base class for Views. Views are groupings of UI elements
    that are displayed in the dashboard.
    """

    @abstractmethod
    def update(self) -> None:
        """Abstract method to update elements in a view"""


class EntityView(ViewBase):
    """View class for entities. Entities include
    Applications, Orchestrators, Shards, Ensembles, and Members.

    EntityViews are a collection of UI elements and have logs and
    statuses that update.
    """

    def __init__(self, view_model: t.Optional[t.Dict[str, t.Any]]) -> None:
        """Initialize an EntityView

        :param view_model: Selected entity view
        :type view_model: Optional[Dict[str, Any]]
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
        return get_logs(file=get_value("err_file", self.view_model))

    @property
    def out_logs(self) -> str:
        """Get output logs from selected entity view

        :return: Output logs
        :rtype: str
        """
        return get_logs(file=get_value("out_file", self.view_model))

    def update(self) -> None:
        """Update logs and status elements in the selected entity view"""
        self.update_logs()
        self.update_status()

    def update_logs(self) -> None:
        """Update error and output log elements in the selected entity view"""
        self.out_logs_element.code(self.out_logs, language=None)
        self.err_logs_element.code(self.err_logs, language=None)

    @abstractmethod
    def update_status(self) -> None:
        """Abstract method to update an entity's status"""

    def update_view_model(self, new_view_model: t.Optional[t.Dict[str, t.Any]]) -> None:
        """Update view_model

        This is called after a new entity is selected
        in the dashboard to keep displayed data in sync.

        :param new_view_model: Selected entity view
        :type new_view_model: Optional[Dict[str, Any]]
        """
        if new_view_model is not None:
            self.view_model = new_view_model


class ExperimentView(ViewBase):
    """View class for experiments"""

    def __init__(
        self,
        experiment: t.Optional[t.Dict[str, t.Any]],
        runs: t.List[t.Dict[str, t.Any]],
    ) -> None:
        """Initialize an ExperimentView

        :param experiment: Experiment
        :type experiment: Optional[Dict[str, Any]]
        :param runs: Runs within an experiment
        :type runs: List[Dict[str, Any]]
        """
        self.status_element = DeltaGenerator()
        self.experiment = experiment
        self.runs = runs

    @property
    def status(self) -> str:
        """Get experiment status

        :return: Experiment status
        :rtype: str
        """
        return get_experiment_status_summary(self.runs)

    def update(self) -> None:
        """Update status element in ExperimentView"""
        self.status_element.write(self.status)


class ApplicationView(EntityView):
    """View class for applications"""

    def __init__(self, application: t.Optional[t.Dict[str, t.Any]]) -> None:
        """Initialize an ApplicationView

        :param application: Selected application
        :type application: Optional[Dict[str, Any]]
        """
        self.status_element = DeltaGenerator()
        super().__init__(view_model=application)

    @property
    def application(self) -> t.Optional[t.Dict[str, t.Any]]:
        """Get application associated with the view model

        :return: Selected application
        :rtype: Optional[Dict[str, Any]]
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
                status = get_status(
                    self.application["telemetry_metadata"]["status_dir"]
                )
            except KeyError:
                status = StatusData(StatusEnum.UNKNOWN, None)
            return format_status(status)
        return "Status: "

    def update_status(self) -> None:
        """Update status element in ApplicationView"""
        self.status_element.write(self.status)


class OrchestratorView(EntityView):
    """View class for orchestrators"""

    def __init__(
        self,
        orchestrator: t.Optional[t.Dict[str, t.Any]],
        shard: t.Optional[t.Dict[str, t.Any]],
    ) -> None:
        """Initialize an OrchestratorView

        :param orchestrator: Selected orchestrator
        :type orchestrator: Optional[Dict[str, Any]]
        :param shard: Selected shard within the selected orchestrator
        :type shard: Optional[Dict[str, Any]]
        """
        self.orchestrator = orchestrator
        self.status_element = DeltaGenerator()
        super().__init__(view_model=shard)

    @property
    def shard(self) -> t.Optional[t.Dict[str, t.Any]]:
        """Get shard associated with the view model

        :return: Selected shard
        :rtype: Optional[Dict[str, Any]]
        """
        return self.view_model

    @property
    def status(self) -> str:
        """Get orchestrator status summary

        :return: Status summary
        :rtype: str
        """
        return get_orchestrator_status_summary(self.orchestrator)

    def update_status(self) -> None:
        """Update status element in OrchestratorView"""
        self.status_element.write(self.status)


class EnsembleView(EntityView):
    """View class for ensembles"""

    def __init__(
        self,
        ensemble: t.Optional[t.Dict[str, t.Any]],
        member: t.Optional[t.Dict[str, t.Any]],
    ) -> None:
        """Initialize an EnsembleView

        :param ensemble: Selected ensemble
        :type ensemble: Optional[Dict[str, Any]]
        :param member: Selected member
        :type member: Optional[Dict[str, Any]]
        """
        self.ensemble = ensemble
        self.status_element = DeltaGenerator()
        self.member_status_element = DeltaGenerator()
        super().__init__(view_model=member)

    @property
    def member(self) -> t.Optional[t.Dict[str, t.Any]]:
        """Get member associated with the view model

        :return: Selected member
        :rtype: Optional[Dict[str, Any]]
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
                status = get_status(self.member["telemetry_metadata"]["status_dir"])
            except KeyError:
                status = StatusData(StatusEnum.UNKNOWN, None)
            return format_status(status)
        return "Status: "

    def update_status(self) -> None:
        """Update ensemble and member status elements in EnsembleView"""
        self.status_element.write(self.status)
        self.member_status_element.write(self.member_status)


class ErrorView(ViewBase):
    """View class for errors

    Contains UI elements for static display of unexpected exception
    information.
    """

    def update(self) -> None:
        ...


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

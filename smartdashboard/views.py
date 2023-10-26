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
    @abstractmethod
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
        self.out_logs_element.code(self.out_logs, language=None)
        self.err_logs_element.code(self.err_logs, language=None)

    @abstractmethod
    def update_status(self) -> None:
        pass

    def update_view_model(self, new_view_model: t.Optional[t.Dict[str, t.Any]]) -> None:
        if new_view_model is not None:
            self.view_model = new_view_model


class ExperimentView(ViewBase):
    def __init__(
        self,
        experiment: t.Optional[t.Dict[str, t.Any]],
        runs: t.List[t.Dict[str, t.Any]],
    ) -> None:
        self.status_element = DeltaGenerator()
        self.experiment = experiment
        self.runs = runs

    @property
    def status(self) -> str:
        return get_experiment_status_summary(self.runs)

    def update(self) -> None:
        self.status_element.write(self.status)


class ApplicationView(EntityView):
    def __init__(self, application: t.Optional[t.Dict[str, t.Any]]) -> None:
        self.status_element = DeltaGenerator()
        super().__init__(view_model=application)

    @property
    def application(self) -> t.Optional[t.Dict[str, t.Any]]:
        return self.view_model

    @property
    def status(self) -> str:
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
        self.status_element.write(self.status)


class OrchestratorView(EntityView):
    def __init__(
        self,
        orchestrator: t.Optional[t.Dict[str, t.Any]],
        shard: t.Optional[t.Dict[str, t.Any]],
    ) -> None:
        self.orchestrator = orchestrator
        self.status_element = DeltaGenerator()
        super().__init__(view_model=shard)

    @property
    def shard(self) -> t.Optional[t.Dict[str, t.Any]]:
        return self.view_model

    @property
    def status(self) -> str:
        return get_orchestrator_status_summary(self.orchestrator)

    def update_status(self) -> None:
        self.status_element.write(self.status)


class EnsembleView(EntityView):
    def __init__(
        self,
        ensemble: t.Optional[t.Dict[str, t.Any]],
        member: t.Optional[t.Dict[str, t.Any]],
    ) -> None:
        self.ensemble = ensemble
        self.status_element = DeltaGenerator()
        self.member_status_element = DeltaGenerator()
        super().__init__(view_model=member)

    @property
    def member(self) -> t.Optional[t.Dict[str, t.Any]]:
        return self.view_model

    @property
    def status(self) -> str:
        return get_ensemble_status_summary(self.ensemble)

    @property
    def member_status(self) -> str:
        if self.member is not None:
            try:
                status = get_status(self.member["telemetry_metadata"]["status_dir"])
            except KeyError:
                status = StatusData(StatusEnum.UNKNOWN, None)
            return format_status(status)
        return "Status: "

    def update_status(self) -> None:
        self.status_element.write(self.status)
        self.member_status_element.write(self.member_status)


class ErrorView(ViewBase):
    def update(self) -> None:
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

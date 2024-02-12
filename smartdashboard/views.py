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
from dataclasses import dataclass
import pathlib

import altair as alt
import pandas as pd
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
                status = StatusData(StatusEnum.UNKNOWN, None)
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
                status = StatusData(StatusEnum.UNKNOWN, None)
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

    def update(self) -> None:
        ...


class OverviewView(ViewBase):
    """View class for the collection of Experiment Overview views"""

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

    def update(self) -> None:
        """Update all views within the OverviewView"""
        self.exp_view.update()
        self.app_view.update()
        self.ens_view.update()
        self.orc_view.update()


@dataclass
class DataContext:
    path: pathlib.Path = pathlib.Path()
    dframe: t.Optional[pd.DataFrame] = pd.DataFrame()
    cols: pd.Index = pd.Index([])
    index: int = 0
    min: int = 0

    @property
    def max_records(self) -> int:
        return 1000


@dataclass
class DualView(ViewBase):
    shard: t.Optional[Shard]
    table_element: DeltaGenerator
    graph_element: DeltaGenerator
    chart: t.Optional[alt.Chart] = None
    data_ctx = DataContext()

    @property
    @abstractmethod
    def _metric_path(self) -> str:
        ...

    @property
    def metric_path(self) -> str:
        return self._metric_path

    def initialize_data(self) -> None:
        if self.shard is not None:
            try:
                self.data_ctx = DataContext()

                self.data_ctx.path = pathlib.Path(self.metric_path)

                # self.data_ctx.dframe = _load_data(
                #     self.data_ctx.path, 0, self.data_ctx.max_records
                # )

                _, self.data_ctx.dframe = _load_data(
                    self.data_ctx.path, 0, self.data_ctx.max_records, None
                )
                if self.data_ctx.dframe is not None:
                    self.data_ctx.cols = self.data_ctx.dframe.columns
                    self.data_ctx.index = 0
                    # self.data_ctx.index = self.data_ctx.max_records - subtract_from_index
                    self.data_ctx.min = self.data_ctx.dframe.timestamp.min()

            except ValueError:
                self.table_element.info(
                    f"Telemetry information could not be found for {self.shard.name}."
                )
                return

    @abstractmethod
    def _update_table(self, dframe: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def _update_graph(self, dframe: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def update(self) -> None:
        ...
    def update(self) -> None:
        """Update memory table and graph elements for selected shard"""
        if self.shard is not None:
            if self.data_ctx.dframe is None:
                # self.data_ctx.dframe = _load_data(
                #     self.data_ctx.path,
                #     self.data_ctx.index,
                #     self.data_ctx.max_records,

                # )

                subtract_from_index, self.data_ctx.dframe = _load_data(
                    self.data_ctx.path,
                    self.data_ctx.index,
                    self.data_ctx.max_records,
                    self.data_ctx.cols
                )
                self.data_ctx.index -= subtract_from_index


            self.data_ctx.dframe.columns = self.data_ctx.cols
            # self._update_table(self.data_ctx.dframe)
            # self.data_ctx.dframe, temp_idx = load_data(
            #     self.data_ctx.path, self.data_ctx.index, self.data_ctx.max_records
            # )
            self.data_ctx.dframe, temp_idx = load_data(
                self.data_ctx.path, self.data_ctx.index, self.data_ctx.max_records, self.data_ctx.cols
            )

            self._update_table(self.data_ctx.dframe.copy(deep=True))
            self._update_graph(self.data_ctx.dframe)
            if temp_idx == 0:
                self.data_ctx.dframe = None
            else:
                self.data_ctx.index = temp_idx

            print(self.data_ctx.index)



@dataclass
class MemoryView(DualView):
    """View class for memory section of the Database Telemetry page"""

    @property
    def _metric_path(self) -> str:
        if self.shard is not None:
            return self.shard.memory_file
        return ""

    def _update_graph(self, dframe: pd.DataFrame) -> None:
        """Update memory graph for selected shard

        :param dframe: DataFrame with memory data
        :type dframe: pandas.DataFrame
        """

        def process_dataframe(dframe: pd.DataFrame) -> pd.DataFrame:
            gb_columns = [
                "used_memory",
                "used_memory_peak",
                "total_system_memory",
            ]
            dframe[gb_columns] /= 1024**3
            dframe = dframe.rename(
                columns={
                    "used_memory": "Used Memory (GB)",
                    "used_memory_peak": "Used Peak Memory (GB)",
                    "total_system_memory": "Total System Memory (GB)",
                }
            )
            dframe["timestamp"] = dframe["timestamp"] - self.data_ctx.min
            return dframe

        dframe.columns = self.data_ctx.cols
        dframe = process_dataframe(dframe)
        dframe = dframe.drop(columns=["Total System Memory (GB)"])
        dframe_long = dframe.melt(
            "timestamp", var_name="Metric", value_name="Memory (GB)"
        )
        if self.chart is None:
            self.chart = (
                alt.Chart(dframe_long)
                .mark_line()
                .encode(
                    x=alt.X(
                        "timestamp:O",
                        axis=alt.Axis(title="Time in seconds", labelAngle=0),
                    ),
                    y=alt.Y("Memory (GB):Q", axis=alt.Axis(title="Memory in GB")),
                    color=alt.Color(  # type: ignore[no-untyped-call]
                        "Metric:N", scale=alt.Scale(scheme="category10"), title="Legend"
                    ),
                    tooltip=["timestamp:O", "Metric:N", "Memory (GB):Q"],
                )
                .properties(
                    height=500, title=alt.TitleParams("Memory Usage", anchor="middle")
                )
                .configure_legend(orient="bottom")
            )
            self.graph_element.altair_chart(
                self.chart, use_container_width=True, theme="streamlit"
            )

        else:
            self.graph_element.add_rows(dframe_long)

    def _update_table(self, dframe: pd.DataFrame) -> None:
        """Update memory table for selected shard

        :param dframe: DataFrame with memory data
        :type dframe: pandas.DataFrame
        """

        def process_dataframe(dframe: pd.DataFrame) -> pd.DataFrame:
            gb_columns = [
                "used_memory",
                "used_memory_peak",
                "total_system_memory",
            ]
            dframe[gb_columns] /= 1024**3
            dframe = dframe.rename(
                columns={
                    "used_memory": "Used Memory (GB)",
                    "used_memory_peak": "Used Peak Memory (GB)",
                    "total_system_memory": "Total System Memory (GB)",
                }
            )
            dframe = dframe.drop(columns=["timestamp"])
            return dframe

        dframe.columns = self.data_ctx.cols
        dframe = process_dataframe(dframe)
        self.table_element.dataframe(
            dframe.tail(1), use_container_width=True, hide_index=True
        )


def _load_data(
    csv_path: pathlib.Path,
    start_idx: int,
    num_rows: int,
    headers:t.Optional[pd.Index],
    has_header: bool = True,
) -> t.Optional[pd.DataFrame]:
    if not csv_path.exists():
        raise ValueError("The supplied data file does not exist.")

    try:
        # skip_header = start_idx > 0
        header_row = 0 if has_header else None
        # num_extra_skips = 1 if header_row is not None else 0
        # if skip_header:
        #     header_row = None

        dframe = pd.read_csv(
            csv_path,
            header=header_row,
            skiprows=start_idx,  # + num_extra_skips,
            nrows=num_rows,
        )

        max_index = dframe.shape[0]
        subtract_from_index=0
        if headers is not None:
            dframe.columns = headers
        dframe = dframe[dframe["timestamp"] < dframe["timestamp"].max()]
        subtract_from_index = max_index-dframe.shape[0]

    except pd.errors.EmptyDataError:
        dframe = None
        subtract_from_index = 0

    # return dframe
    return subtract_from_index, dframe


def load_data(
    csv_path: pathlib.Path, start_index: int, num_rows: int = 1000, headers: t.Optional[pd.Index] = None,
) -> t.Tuple[t.Optional[pd.DataFrame], int]:
    last_index = start_index + num_rows
    subtract_from_index, dframe = _load_data(csv_path, start_index, num_rows, headers)
    next_index = last_index - subtract_from_index
    # dframe = _load_data(csv_path, start_index, num_rows)
    # next_index = last_index

    if dframe is None:
        next_index = 0
    # elif dframe.shape[0] < num_rows:
    #     next_index = 0

    return dframe, next_index



@dataclass
class ClientView(DualView):
    """View class for client section of the Database Telemetry page"""

    @property
    def _metric_path(self) -> str:
        if self.shard is not None:
            return self.shard.client_file
        return ""

    def _update_graph(self, dframe: pd.DataFrame) -> None:
        """Update client graph for selected shard

        :param dframe: DataFrame with client data
        :type dframe: pandas.DataFrame
        """

        def process_dataframe(dframe: pd.DataFrame) -> pd.DataFrame:
            # when we update, the group by is going to give us 1....N
            # as the timestamp again
            # we need to add the last timestamp to each new batch...
            # ctx.min - 1
            # mod = dframe.copy(deep=True).groupby("timestamp").count()
            # mod["timestamp"] = range(mod.shape[0])
            # mod.columns = ["trash", "num_clients", "timestamp"]
            # mod = mod.set_index("timestamp")
            mod = (
                dframe.copy(deep=True)
                .groupby("timestamp")
                .size()
                .reset_index(name="num_clients")
            )
            mod["timestamp"] = mod["timestamp"] - self.data_ctx.min
            return mod

        if self.chart is None:
            dframe.columns = self.data_ctx.cols
            self.chart = (
                alt.Chart(process_dataframe(dframe))
                .mark_line()
                .encode(
                    x=alt.X("timestamp:Q", axis=alt.Axis(title="Time in seconds")),
                    y=alt.Y("num_clients:Q", axis=alt.Axis(title="Client Count")),
                    tooltip=["timestamp:Q", "num_clients:Q"],
                )
                .properties(
                    height=500,
                    title=alt.TitleParams("Total Client Count", anchor="middle"),
                )
            )
            self.graph_element.altair_chart(self.chart, use_container_width=True)

        else:
            dframe.columns = self.data_ctx.cols
            self.graph_element.add_rows(process_dataframe(dframe))

    def _update_table(self, dframe: pd.DataFrame) -> None:
        """Update client table for selected shard

        :param dframe: DataFrame with client data
        :type dframe: pandas.DataFrame
        """

        def process_dataframe(dframe: pd.DataFrame) -> pd.DataFrame:
            dframe = dframe.loc[dframe["timestamp"] == dframe["timestamp"].max()]
            dframe = dframe.drop(columns=["timestamp"])
            dframe = dframe.rename(
                columns={
                    "client_id": "Client ID",
                    "address": "Address",
                }
            )
            return dframe

        dframe.columns = self.data_ctx.cols
        self.table_element.dataframe(
            process_dataframe(dframe), use_container_width=True, hide_index=True
        )


class OrchestratorSummaryView(ViewBase):
    """View class for orchestrator summary section of the Database Telemetry page"""

    def __init__(self, orchestrator: t.Optional[Orchestrator]) -> None:
        """Initialize an OrchestratorSummaryView

        :param orchestrator: Selected orchestrator
        :type orchestrator: t.Optional[Orchestrator]
        """
        self.orchestrator = orchestrator
        self.status_element = DeltaGenerator()

    @property
    def status(self) -> str:
        """Get orchestrator status summary

        :return: Status summary
        :rtype: str
        """
        return get_orchestrator_status_summary(self.orchestrator)

    def update(self) -> None:
        """Update status element in OrchestratorView"""
        self.status_element.write(self.status)


class TelemetryView(ViewBase):
    """View class for the collection of Database Telemetry views"""

    def __init__(
        self,
        orc_summary_view: OrchestratorSummaryView,
        memory_view: MemoryView,
        client_view: ClientView,
    ) -> None:
        """Initialize a TelemetryView

        :param orc_summary_view: OrchestratorSummaryView rendered in the dashboard
        :type orc_summary_view: OrchestratorSummaryView
        :param memory_view: MemoryView rendered in the dashboard
        :type memory_view: MemoryView
        :param client_view: ClientView view rendered in the dashboard
        :type client_view: ClientView
        """
        self.orc_summary_view = orc_summary_view
        self.memory_view = memory_view
        self.client_view = client_view

    def update(self) -> None:
        """Update all views within the TelemetryView"""
        self.orc_summary_view.update()
        self.memory_view.update()
        self.client_view.update()

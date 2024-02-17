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
import streamlit as st

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

    def update(self) -> None: ...


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
class MemoryView(ViewBase):
    """View class for memory section of the Database Telemetry page"""

    def __init__(
        self, shard, memory_table_element, memory_graph_element, export_button
    ):
        self.shard = shard
        self.memory_table_element = memory_table_element
        self.memory_graph_element = memory_graph_element
        self.export_button = export_button
        self.telemetry=True

        if "memory_df" not in st.session_state:
            # Only put the historical data into session state if we haven't already loaded
            try:
                df = self.load_data()
                self._set_df(df)
            except FileNotFoundError as e:
                self.memory_table_element.info(
                    f"Memory information could not be found for {self.shard.name}"
                )
                self.telemetry = False
            # else:
                # self.telemetry = False
        else:
            df = self._df()

        if self.shard is not None and self.telemetry:
            export_button.download_button(
                label="Export Data",
                data=self.get_memory_file(),
                file_name=f"{self.shard.name}_memory.csv",
                mime="text/csv",
            )

        self.window_size = 10000
        if self.telemetry:
            self.timestamp_min = st.session_state["memory_df"]["timestamp"].min()
            self._handle_data()


    def _handle_data(self):
        table_df = st.session_state["memory_df"].copy(deep=True)
        graph_df:pd.DataFrame = st.session_state["memory_df"].copy(deep=True)
        if st.session_state["memory_df"].shape[0] >= self.window_size:
            graph_df = graph_df.sample(10000)

        self._update_memory_table(self.process_dataframe(table_df))
        self._update_memory_graph(self.process_dataframe(graph_df))

    def get_memory_file(self):
        return pd.read_csv(self.shard.memory_file).to_csv()

    @st.cache_data
    def load_data(self) -> pd.DataFrame:
        """Load the datasource into a DataFrame and return it; caching necessitates live
        data updates to place dataframe in st.session_state and concatenate new data"""
        if self.shard is not None and self.telemetry:
            df = pd.read_csv(self.shard.memory_file)
            st.session_state["memory_df"] = df
            return df

    def load_data_update(self, skiprows: int) -> pd.DataFrame:
        if self.shard is not None and self.telemetry:
            try:
                df = pd.read_csv(self.shard.memory_file, skiprows=range(1, skiprows))
                st.session_state["memory_df_upd"] = df
                return df
            except FileNotFoundError:
                self.memory_table_element.info(
                    f"Memory information could not be found for {self.shard.name}"
                )

    def process_dataframe(self, dframe: pd.DataFrame) -> pd.DataFrame:
        gb_columns = [
            "used_memory",
            "used_memory_peak",
            "total_system_memory",
        ]
        dframe[gb_columns] /= 1024**3
        dframe = dframe.rename(
            columns={
                "used_memory": "Used Memory (GB)",
                "used_memory_peak": "Used Memory Peak (GB)",
                "total_system_memory": "Total System Memory (GB)",
            }
        )
        dframe["timestamp"] = dframe["timestamp"] - self.timestamp_min
        return dframe

    def update(self) -> None:
        if self.shard is not None and self.telemetry:
            df_delta = self.load_data_update(
                skiprows=st.session_state["memory_df"].shape[0] + 1
            )
            self._set_df_delta(df_delta)
            if not df_delta.empty:
                #graph isf there's new data
                df = pd.concat((st.session_state["memory_df"], df_delta), axis=0)
                self._set_df(df)
                self._handle_data()

    def _df(self) -> pd.DataFrame:
        df = st.session_state["memory_df"]
        return df

    def _set_df(self, df: pd.DataFrame) -> None:
        st.session_state["memory_df"] = df

    def _df_delta(self) -> pd.DataFrame:
        df = st.session_state["memory_df_delta"]
        return df

    def _set_df_delta(self, df: pd.DataFrame) -> None:
        st.session_state["memory_df_delta"] = df

    def _update_memory_graph(self, dframe: pd.DataFrame) -> None:
        """Update memory graph for selected shard

        :param dframe: DataFrame with memory data
        :type dframe: pandas.DataFrame
        """

        dframe = dframe.drop(columns=["Total System Memory (GB)"])
        dframe_long = dframe.melt(
            "timestamp", var_name="Metric", value_name="Memory (GB)"
        )
        chart = (
            alt.Chart(dframe_long)
            .mark_line()
            .encode(
                x=alt.X(
                    "timestamp:O",
                    axis=alt.Axis(title="Timestep in seconds", labelAngle=0),
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

        self.memory_graph_element.altair_chart(
            chart, use_container_width=True, theme="streamlit"
        )

    def _update_memory_table(self, dframe: pd.DataFrame) -> None:
        """Update memory table for selected shard

        :param dframe: DataFrame with memory data
        :type dframe: pandas.DataFrame
        """

        dframe = dframe.drop(columns=["timestamp"])
        self.memory_table_element.dataframe(
            dframe.tail(1), use_container_width=True, hide_index=True
        )


@dataclass()
class ClientView(ViewBase):
    """View class for client section of the Database Telemetry page"""

    shard: t.Optional[Shard]
    client_table_element: DeltaGenerator
    client_graph_element: DeltaGenerator
    manual_element: DeltaGenerator
    slider_element: DeltaGenerator
    sample_element: DeltaGenerator
    st.session_state["counts_df"] = pd.DataFrame()
    clients_df = pd.DataFrame()
    timestamp_min = 0
    _manual: bool = False
    key = 0
    min = 0
    max = 14000

    CLIENT_KEY_SLIDER = "client_slider"

    def set_max(self) -> None:
        new_max = st.session_state["counts_df"]["timestamp"].max()
        self.max = new_max
        # st.session_state[self.KEY_SLIDER] = (new_max-10000,new_max)
        # st.session_state[self.KEY_SLIDER] = new_max

    def manual_switch(self) -> bool:
        return not self._manual

    def sample(self): ...

    def update(self) -> None:
        """Update client table and graph elements for selected shard"""
        if self.shard is not None:
            try:
                self.client_df = pd.read_csv(self.shard.client_file)
                st.session_state["counts_df"] = pd.read_csv(
                    self.shard.client_count_file
                )
                self.timestamp_min = st.session_state["counts_df"]["timestamp"].min()
                self.set_max()

                self._update_client_table(self.client_df)

                if st.session_state["counts_df"].shape[0] > 10000:
                    self._update_client_graph(
                        st.session_state["counts_df"][self.max - 10000 : self.max]
                    )
                    # self.key += 1
                    # clicked = self.sample_element.button(
                    #     "Sample Data",
                    #     on_click=self.sample,
                    #     key=f"client_button_{self.key}",
                    # )
                    # if clicked:
                    #     self.sample()
                    # else:
                    #     self._update_client_graph(
                    #         st.session_state["counts_df"][-10000:]
                    #     )
                else:
                    self._update_client_graph(st.session_state["counts_df"])
            except FileNotFoundError:
                self.client_table_element.info(
                    f"Client data was not found for {self.shard.name}"
                )
        # elif self.shard is not None and self._manual:
        #     self.manual_stuff()

    # def manual_stuff(self) -> None:
    #     # self.key += 1
    #     if self.slider_element == st.empty():
    #         self.min, self.max = self.slider_element.slider(
    #             "Data Slider",
    #             st.session_state["counts_df"]["timestamp"].min(),
    #             st.session_state["counts_df"]["timestamp"].max(),
    #             value=[
    #                 st.session_state["counts_df"]["timestamp"].max() - 10000,
    #                 st.session_state["counts_df"]["timestamp"].max(),
    #             ],
    #             key=f"client_slider",
    #         )
    #         self._update_client_graph(
    #             st.session_state["counts_df"][self.min : self.max]
    #         )
    #     else:
    #         print(st.session_state["client_slider"])

    def _update_client_table(self, dframe: pd.DataFrame) -> None:
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

        self.client_table_element.dataframe(
            process_dataframe(dframe), use_container_width=True, hide_index=True
        )

    def _update_client_graph(self, dframe: pd.DataFrame) -> None:
        """Update client graph for selected shard

        :param dframe: DataFrame with client data
        :type dframe: pandas.DataFrame
        """

        def process_dataframe(dframe: pd.DataFrame) -> pd.DataFrame:
            dframe["timestamp"] = dframe["timestamp"] - self.timestamp_min
            # dframe = dframe.drop(columns=["timestamp"])
            return dframe

        chart = (
            alt.Chart(process_dataframe(dframe))
            .mark_line()
            .encode(
                x=alt.X("timestamp:Q", axis=alt.Axis(title="Timestep")),
                y=alt.Y("num_clients:Q", axis=alt.Axis(title="Client Count")),
                tooltip=["timestamp:Q", "num_clients:Q"],
            )
            .properties(
                height=500,
                title=alt.TitleParams("Total Client Count", anchor="middle"),
            )
        )

        self.client_graph_element.altair_chart(chart, use_container_width=True)


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

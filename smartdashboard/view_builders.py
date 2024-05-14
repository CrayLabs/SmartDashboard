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

import traceback
import typing as t

import pandas as pd
import streamlit as st

from smartdashboard.schemas.orchestrator import Orchestrator
from smartdashboard.schemas.shard import Shard
from smartdashboard.utils.errors import SSDashboardError
from smartdashboard.utils.helpers import (
    build_dataframe_generic,
    build_dataframe_loaded_entities,
    flatten_nested_keyvalue_containers,
    format_ensemble_params,
    format_interfaces,
    get_port,
    render_dataframe,
    shard_log_spacing,
)
from smartdashboard.utils.ManifestReader import Manifest
from smartdashboard.views import (
    ApplicationView,
    ClientView,
    DatabaseTelemetryView,
    EnsembleView,
    ErrorView,
    ExperimentView,
    MemoryView,
    OrchestratorSummaryView,
    OrchestratorView,
    OverviewView,
)


def error_builder(error: SSDashboardError) -> ErrorView:
    """Error view displayed when errors are caught

    :param error: Error to get information from
    :type error: SSDashboardError
    :return: An error view
    :rtype: ErrorView
    """
    view = ErrorView()
    st.header(str(error))
    # fmt: off
    st.error(
        f"""Error found in file: {error.file}  
             Error Message: {error.exception}"""
    )
    # fmt: on

    with st.expander(label="Traceback"):
        st.code(traceback.format_exc(), language="log")

    return view


def exp_builder(manifest: Manifest) -> ExperimentView:
    """Experiment view to be rendered

    :param manifest: Manifest to get dashboard info from
    :type manifest: Manifest
    :return: An experiment view
    :rtype: ExperimentView
    """
    view = ExperimentView(manifest.experiment, manifest.runs)
    st.subheader("Experiment Configuration")
    st.write("")
    view.status_element = st.empty()
    st.write("Path: " + manifest.experiment.path)
    st.write("Launcher: " + manifest.experiment.launcher)

    with st.expander(label="Logs", expanded=True):
        col1, col2 = st.columns([6, 6])
        with col1:
            st.write("Output")
            view.out_logs_element = st.code(view.out_logs, language="log")

        with col2:
            st.write("Error")
            view.err_logs_element = st.code(view.err_logs, language="log")

    return view


def app_builder(manifest: Manifest) -> ApplicationView:
    """Application view to be rendered

    :param manifest: Manifest to get dashboard info from
    :type manifest: Manifest
    :return: An application view
    :rtype: ApplicationView
    """
    st.subheader("Application Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_application_context = st.selectbox(
            "Select an application:",
            manifest.apps_with_run_ctx,
            format_func=lambda context: f"{context.entity.name}: Run {context.run_id}",
        )

    if selected_application_context is not None:
        selected_application = selected_application_context.entity
    else:
        selected_application = None

    view = ApplicationView(selected_application)

    st.write("")
    view.status_element = st.empty()
    st.write("Path: " + (view.application.path if view.application is not None else ""))

    st.write("")
    with st.expander(label="Executable Arguments"):
        arguments = (
            selected_application.exe_args if selected_application is not None else []
        )
        render_dataframe(pd.DataFrame(arguments, columns=["All Arguments"]))

    st.write("")
    with st.expander(label="Batch and Run Settings"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Batch Settings",
            dict_name="batch_settings",
            entity=selected_application.dict() if selected_application else {},
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Run Settings",
            dict_name="run_settings",
            entity=selected_application.dict() if selected_application else {},
            df_columns=["Name", "Value"],
        )

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Parameters",
            dict_name="params",
            entity=selected_application.dict() if selected_application else {},
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Files",
            dict_name="files",
            entity=selected_application.dict() if selected_application else {},
            df_columns=["Type", "File"],
        )

    st.write("")
    with st.expander(label="Colocated Database"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            app_colocated_db: t.Optional[t.Dict[str, t.Any]] = (
                selected_application.colocated_db
                if selected_application is not None
                else {}
            )
            build_dataframe_generic(
                column=col1,
                title="Summary",
                dict_name="settings",
                entity=app_colocated_db,
                df_columns=["Name", "Value"],
            )
            build_dataframe_loaded_entities(
                column=col2,
                title="Loaded Scripts and Models",
                entity=selected_application,
            )

    st.write("")
    with st.expander(label="Logs"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            with col1:
                st.write("Output")
                view.out_logs_element = st.code(view.out_logs, language="log")

            with col2:
                st.write("Error")
                view.err_logs_element = st.code(view.err_logs, language="log")

    return view


def orc_builder(manifest: Manifest) -> OrchestratorView:
    """Orchestrator view to be rendered

    :param manifest: Manifest to get dashboard info from
    :type manifest: Manifest
    :return: An orchestrator view
    :rtype: OrchestratorView
    """
    st.subheader("Orchestrator Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_orchestrator_context = st.selectbox(
            "Select an orchestrator:",
            manifest.orcs_with_run_ctx,
            format_func=lambda context: f"{context.entity.name}: Run {context.run_id}",
        )

    if selected_orchestrator_context is not None:
        selected_orchestrator = selected_orchestrator_context.entity
    else:
        selected_orchestrator = None

    shards = selected_orchestrator.shards if selected_orchestrator else []
    view = OrchestratorView(selected_orchestrator, shards[0] if shards else None)

    st.write("")
    view.status_element = st.empty()
    st.write(
        "Type: "
        + (selected_orchestrator.type if selected_orchestrator is not None else "")
    )
    st.write("Port: " + get_port(selected_orchestrator))
    st.write("Interface: " + format_interfaces(selected_orchestrator))

    st.write("")
    with st.expander(label="Database Hosts"):
        hosts = selected_orchestrator.db_hosts if selected_orchestrator else []
        render_dataframe(pd.DataFrame(hosts, columns=["Hosts"]))

    st.write("")
    with st.expander(label="Logs"):
        col1, col2 = st.columns([6, 6])
        with col1:
            shard = st.selectbox(
                "Select a shard:", shards, format_func=lambda shard: shard.name
            )

            view.update_view_model(shard)

            st.write("")
            st.write("Output")
            view.out_logs_element = st.code(view.out_logs, language="log")

        with col2:
            shard_log_spacing()
            st.write("Error")
            view.err_logs_element = st.code(view.err_logs, language="log")

    return view


def ens_builder(manifest: Manifest) -> EnsembleView:
    """Ensemble view to be rendered

    :param manifest: Manifest to get dashboard info from
    :type manifest: Manifest
    :return: An ensemble view
    :rtype: EnsembleView
    """
    st.subheader("Ensemble Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_ensemble_context = st.selectbox(
            "Select an ensemble:",
            manifest.ensemble_with_run_ctx,
            format_func=lambda context: f"{context.entity.name}: Run {context.run_id}",
        )

    if selected_ensemble_context is not None:
        selected_ensemble = selected_ensemble_context.entity
    else:
        selected_ensemble = None

    members = selected_ensemble.models if selected_ensemble else []

    view = EnsembleView(selected_ensemble, members[0] if members else None)

    st.write("")
    view.status_element = st.empty()

    st.write("")
    with st.expander(label="Batch Settings"):
        batch = flatten_nested_keyvalue_containers(
            "batch_settings",
            selected_ensemble.dict() if selected_ensemble else {},
        )
        render_dataframe(pd.DataFrame(batch, columns=["Name", "Value"]))

    st.write("")
    with st.expander(label="Parameters"):
        params = format_ensemble_params(selected_ensemble)
        render_dataframe(pd.DataFrame(params, columns=["Name", "Value"]))

    st.write("#")
    if selected_ensemble is not None:
        st.subheader(selected_ensemble.name + " Member Configuration")
    else:
        st.subheader("Member Configuration")

    col1, col2 = st.columns([4, 4])
    with col1:
        member = st.selectbox(
            "Select a member:", members, format_func=lambda member: member.name
        )

    view.update_view_model(member)

    st.write("")
    view.member_status_element = st.empty()
    st.write("Path: " + (member.path if member else ""))
    st.write("")
    with st.expander(label="Executable Arguments"):
        arguments = member.exe_args if member is not None else []
        render_dataframe(pd.DataFrame(arguments, columns=["All Arguments"]))

    st.write("")
    with st.expander(label="Batch and Run Settings"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Batch Settings",
            dict_name="batch_settings",
            entity=member.dict() if member else {},
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Run Settings",
            dict_name="run_settings",
            entity=member.dict() if member else {},
            df_columns=["Name", "Value"],
        )

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Parameters",
            dict_name="params",
            entity=member.dict() if member else {},
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Files",
            dict_name="files",
            entity=member.dict() if member else {},
            df_columns=["Type", "File"],
        )

    st.write("")
    with st.expander(label="Colocated Database"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            mem_colocated_db: t.Optional[t.Dict[str, t.Any]] = (
                member.colocated_db if member is not None else {}
            )
            build_dataframe_generic(
                column=col1,
                title="Summary",
                dict_name="settings",
                entity=mem_colocated_db,
                df_columns=["Name", "Value"],
            )
            build_dataframe_loaded_entities(
                column=col2,
                title="Loaded Scripts and Models",
                entity=member,
            )

    st.write("")
    with st.expander(label="Logs"):
        col1, col2 = st.columns([6, 6])
        with col1:
            st.write("Output")
            view.out_logs_element = st.code(view.out_logs, language="log")

        with col2:
            st.write("Error")
            view.err_logs_element = st.code(view.err_logs, language="log")

    return view


def overview_builder(manifest: Manifest) -> OverviewView:
    """Experiment Overview page to be rendered

    This function organizes all of the above views
    into their respective tabs inside the dashboard.

    :param manifest: Manifest to get dashboard info from
    :type manifest: Manifest
    :return: View of the entire Overview page
    :rtype: OverviewView
    """
    st.header("Experiment Overview: " + manifest.experiment.name)
    st.write("")

    experiment, application, orchestrators, ensembles = st.tabs(
        ["Experiment", "Applications", "Orchestrators", "Ensembles"]
    )

    ### Experiment ###
    with experiment:
        exp_view = exp_builder(manifest)

    ### Applications ###
    with application:
        app_view = app_builder(manifest)

    ### Orchestrator ###
    with orchestrators:
        orc_view = orc_builder(manifest)

    ### Ensembles ###
    with ensembles:
        ens_view = ens_builder(manifest)

    return OverviewView(exp_view, app_view, orc_view, ens_view)


def db_telem_builder(manifest: Manifest) -> DatabaseTelemetryView:
    """Database Telemetry page to be rendered

    This function organizes the views within
    the Database Telemetry page.

    :param manifest: Manifest of the Experiment
    :type manifest: Manifest
    :return: View of the DB Telemetry Page
    :rtype: TelemetryView
    """
    st.header("Database Telemetry")

    st.write("")

    col1, _ = st.columns([6, 6])
    with col1:
        selected_orchestrator_context = st.selectbox(
            "Select an orchestrator:",
            manifest.orcs_with_run_ctx,
            format_func=lambda context: f"{context.entity.name}: Run {context.run_id}",
        )

    st.write("")

    if selected_orchestrator_context is not None:
        run_id = selected_orchestrator_context.run_id
        selected_orchestrator = selected_orchestrator_context.entity
        shards = selected_orchestrator.shards
        st.subheader(f"{selected_orchestrator.name}: Run {run_id} Telemetry")
    else:
        run_id, selected_orchestrator = None, None
        shards = []
        st.subheader("No Orchestrator Selected")

    st.write("")

    ### Orchestrator Summary ###
    orc_summary_view = orc_summary_builder(selected_orchestrator)
    st.write("")

    ### Memory ###
    memory_view = memory_view_builder(shards)
    st.write("")

    ### Clients ###
    client_view = client_view_builder(shards)
    st.write("")

    return DatabaseTelemetryView(orc_summary_view, memory_view, client_view)


def memory_view_builder(shards: t.List[Shard]) -> MemoryView:
    """Memory section of Database Telemetry page to be rendered

    :param shards: Shards of the selected Orchestrator
    :type shards: t.List[Shard]
    :return: View of the memory portion of the DB Telemetry page
    :rtype: MemoryView
    """

    with st.expander(label="Memory"):
        col1, col2 = st.columns([0.4, 0.5])
        with col1:
            shard = st.selectbox(
                "Select a shard:",
                shards,
                format_func=lambda shard: shard.name,
                key="memory_shard",
            )
            memory_table_element = st.empty()
        with col2:
            st.write("")
            st.write("")
            st.write("")
            memory_graph_element = st.empty()
            _, colb = st.columns([0.85, 0.15])
            with colb:
                export_button = st.empty()

    return MemoryView(shard, memory_table_element, memory_graph_element, export_button)


def client_view_builder(shards: t.List[Shard]) -> ClientView:
    """Client section of Database Telemetry page to be rendered

    :param shards: Shards of the selected Orchestrator
    :type shards: t.List[Shard]
    :return: View of the client portion of the DB Telemetry page
    :rtype: ClientView
    """

    with st.expander(label="Clients"):
        col1, col2 = st.columns([0.4, 0.5])
        with col1:
            shard = st.selectbox(
                "Select a shard:",
                shards,
                format_func=lambda shard: shard.name,
                key="client_shard",
            )
            client_table_element = st.empty()
        with col2:
            st.write("")
            st.write("")
            st.write("")
            client_graph_element = st.empty()
            _, colb = st.columns([0.85, 0.15])
            with colb:
                export_button = st.empty()

    return ClientView(shard, client_table_element, client_graph_element, export_button)


def orc_summary_builder(
    selected_orchestrator: t.Optional[Orchestrator],
) -> OrchestratorSummaryView:
    """Orchestrator summary section of Database Telemetry page to be rendered

    :param selected_orchestrator: Selected Orchestrator
    :type selected_orchestrator: t.Optional[Orchestrator]
    :return: View of the summary portion of the DB Telemetry page
    :rtype: OrchestratorSummaryView
    """
    view = OrchestratorSummaryView(selected_orchestrator)
    data = selected_orchestrator.db_hosts if selected_orchestrator else []

    with st.expander(label="Orchestrator Summary"):

        st.write("")
        view.status_element = st.empty()
        st.write(
            "Number of shards: "
            + (str(len(selected_orchestrator.shards)) if selected_orchestrator else "")
        )
        st.write(
            "Type: "
            + (selected_orchestrator.type if selected_orchestrator is not None else "")
        )
        st.write("Port: " + get_port(selected_orchestrator))
        st.write("Interface: " + format_interfaces(selected_orchestrator))

        st.write("")

        render_dataframe(pd.DataFrame(data, columns=["Hosts"]))

    return view

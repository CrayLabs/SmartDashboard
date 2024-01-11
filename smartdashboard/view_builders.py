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

import traceback
import typing as t

import pandas as pd
import streamlit as st

from smartdashboard.utils.errors import SSDashboardError
from smartdashboard.utils.helpers import (
    build_dataframe_generic,
    build_dataframe_loaded_entities,
    flatten_nested_keyvalue_containers,
    format_ensemble_params,
    get_port,
    render_dataframe,
    shard_log_spacing,
)
from smartdashboard.utils.ManifestReader import Manifest
from smartdashboard.views import (
    ApplicationView,
    EnsembleView,
    ErrorView,
    ExperimentView,
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
    st.error(
        f"""Error found in file: {error.file}  
             Error Message: {error.exception}"""
    )

    with st.expander(label="Traceback"):
        st.code(traceback.format_exc(), language=None)

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
        selected_application = st.selectbox(
            "Select an application:",
            manifest.applications,
            format_func=lambda app: f"{app.name}: Run {app.run_id}",
        )

    view = ApplicationView(selected_application)

    st.write("")
    view.status_element = st.empty()
    st.write("Path: " + (view.application.path if view.application is not None else ""))

    st.write("")
    with st.expander(label="Executable Arguments"):
        render_dataframe(
            pd.DataFrame(
                {
                    "All Arguments": (
                        selected_application.exe_args
                        if selected_application is not None
                        else []
                    ),
                }
            )
        )

    st.write("")
    with st.expander(label="Batch and Run Settings"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Batch Settings",
            dict_name="batch_settings",
            entity=selected_application.model_dump() if selected_application else {},
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Run Settings",
            dict_name="run_settings",
            entity=selected_application.model_dump() if selected_application else {},
            df_columns=["Name", "Value"],
        )

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Parameters",
            dict_name="params",
            entity=selected_application.model_dump() if selected_application else {},
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Files",
            dict_name="files",
            entity=selected_application.model_dump() if selected_application else {},
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
                view.out_logs_element = st.code(view.out_logs, language=None)

            with col2:
                st.write("Error")
                view.err_logs_element = st.code(view.err_logs, language=None)

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
        selected_orchestrator = st.selectbox(
            "Select an orchestrator:",
            manifest.orchestrators,
            format_func=lambda orc: f"{orc.name}: Run {orc.run_id}",
        )

    shards = selected_orchestrator.shards if selected_orchestrator else []
    view = OrchestratorView(selected_orchestrator, shards[0] if shards else None)

    st.write("")
    view.status_element = st.empty()
    st.write(
        "Type: "
        + (selected_orchestrator.type if selected_orchestrator is not None else "")
    )
    st.write("Port: " + get_port(selected_orchestrator))
    st.write(
        "Interface: " + ", ".join(selected_orchestrator.interface)
        if selected_orchestrator
        else ""
    )

    st.write("")
    with st.expander(label="Database Hosts"):
        render_dataframe(
            pd.DataFrame(
                {
                    "Hosts": (
                        selected_orchestrator.db_hosts if selected_orchestrator else []
                    ),
                }
            )
        )
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
            view.out_logs_element = st.code(view.out_logs, language=None)

        with col2:
            shard_log_spacing()
            st.write("Error")
            view.err_logs_element = st.code(view.err_logs, language=None)

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
        selected_ensemble = st.selectbox(
            "Select an ensemble:",
            manifest.ensembles,
            format_func=lambda ens: f"{ens.name}: Run {ens.run_id}",
        )

    members = selected_ensemble.models if selected_ensemble else []

    view = EnsembleView(selected_ensemble, members[0] if members else None)

    st.write("")
    view.status_element = st.empty()

    st.write("")
    with st.expander(label="Batch Settings"):
        render_dataframe(
            pd.DataFrame(
                flatten_nested_keyvalue_containers(
                    "batch_settings",
                    selected_ensemble.model_dump() if selected_ensemble else {},
                ),
                columns=["Name", "Value"],
            )
        )

    st.write("")
    with st.expander(label="Parameters"):
        render_dataframe(
            pd.DataFrame(
                format_ensemble_params(selected_ensemble),
                columns=["Name", "Value"],
            )
        )

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
        render_dataframe(
            pd.DataFrame(
                {"All Arguments": member.exe_args if member is not None else []}
            ),
        )

    st.write("")
    with st.expander(label="Batch and Run Settings"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Batch Settings",
            dict_name="batch_settings",
            entity=member.model_dump() if member else {},
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Run Settings",
            dict_name="run_settings",
            entity=member.model_dump() if member else {},
            df_columns=["Name", "Value"],
        )

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Parameters",
            dict_name="params",
            entity=member.model_dump() if member else {},
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Files",
            dict_name="files",
            entity=member.model_dump() if member else {},
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
            view.out_logs_element = st.code(view.out_logs, language=None)

        with col2:
            st.write("Error")
            view.err_logs_element = st.code(view.err_logs, language=None)

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

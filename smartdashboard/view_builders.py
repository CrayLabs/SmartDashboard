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
    get_all_shards,
    get_db_hosts,
    get_ensemble_members,
    get_entity_from_name,
    get_exe_args,
    get_interfaces,
    get_member,
    get_port,
    get_shard,
    get_value,
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
    st.write("Path: " + manifest.experiment.get("path", ""))
    st.write("Launcher: " + manifest.experiment.get("launcher", ""))

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
        selected_app_name: t.Optional[str] = st.selectbox(
            "Select an application:",
            [f'{app["name"]}: Run {app["run_id"]}' for app in manifest.applications],
        )

    if selected_app_name is not None:
        selected_application = get_entity_from_name(
            selected_app_name, manifest.applications
        )
    else:
        selected_application = None

    view = ApplicationView(selected_application)

    st.write("")
    view.status_element = st.empty()
    st.write("Path: " + get_value("path", view.application))

    st.write("")
    with st.expander(label="Executable Arguments"):
        render_dataframe(
            pd.DataFrame(
                {
                    "All Arguments": get_exe_args(selected_application),
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
            entity=selected_application,
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Run Settings",
            dict_name="run_settings",
            entity=selected_application,
            df_columns=["Name", "Value"],
        )

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Parameters",
            dict_name="params",
            entity=selected_application,
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Files",
            dict_name="files",
            entity=selected_application,
            df_columns=["Type", "File"],
        )

    st.write("")
    with st.expander(label="Colocated Database"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            app_colocated_db: t.Optional[t.Dict[str, t.Any]] = (
                selected_application.get("colocated_db")
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
                column=col2, title="Loaded Scripts and Models", entity=app_colocated_db
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
        selected_orc_name: t.Optional[str] = st.selectbox(
            "Select an orchestrator:",
            [f'{orc["name"]}: Run {orc["run_id"]}' for orc in manifest.orchestrators],
        )

    if selected_orc_name is not None:
        selected_orchestrator = get_entity_from_name(
            selected_orc_name, manifest.orchestrators
        )
    else:
        selected_orchestrator = None

    shards: t.List[t.Dict[str, t.Any]] = get_all_shards(selected_orchestrator)
    view = OrchestratorView(selected_orchestrator, shards[0] if shards else None)

    st.write("")
    view.status_element = st.empty()
    st.write("Type: " + get_value("type", selected_orchestrator))
    st.write("Port: " + get_port(selected_orchestrator))
    st.write("Interface: " + get_interfaces(selected_orchestrator))

    st.write("")
    with st.expander(label="Database Hosts"):
        render_dataframe(
            pd.DataFrame(
                {
                    "Hosts": get_db_hosts(selected_orchestrator),
                }
            )
        )
    st.write("")
    with st.expander(label="Logs"):
        col1, col2 = st.columns([6, 6])
        with col1:
            selected_shard_name: t.Optional[str] = st.selectbox(
                "Select a shard:",
                [shard["name"] for shard in shards if shard is not None],
            )

            if selected_shard_name is not None:
                shard = get_shard(selected_shard_name, selected_orchestrator)
            else:
                shard = None

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
        selected_ensemble_name: t.Optional[str] = st.selectbox(
            "Select an ensemble:",
            [
                f'{ensemble["name"]}: Run {ensemble["run_id"]}'
                for ensemble in manifest.ensembles
            ],
        )

    if selected_ensemble_name is not None:
        selected_ensemble = get_entity_from_name(
            selected_ensemble_name, manifest.ensembles
        )
    else:
        selected_ensemble = None

    members: t.List[t.Dict[str, t.Any]] = get_ensemble_members(selected_ensemble)
    view = EnsembleView(selected_ensemble, members[0] if members else None)

    st.write("")
    view.status_element = st.empty()

    st.write("")
    with st.expander(label="Batch Settings"):
        render_dataframe(
            pd.DataFrame(
                flatten_nested_keyvalue_containers("batch_settings", selected_ensemble),
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
    if selected_ensemble_name is not None:
        st.subheader(selected_ensemble_name + " Member Configuration")
    else:
        st.subheader("Member Configuration")

    col1, col2 = st.columns([4, 4])
    with col1:
        selected_member_name: t.Optional[str] = st.selectbox(
            "Select a member:",
            [member["name"] for member in members if member],
        )

    if selected_member_name is not None:
        member = get_member(selected_member_name, selected_ensemble)
    else:
        member = None

    view.update_view_model(member)

    st.write("")
    view.member_status_element = st.empty()
    st.write("Path: " + get_value("path", member))
    st.write("")
    with st.expander(label="Executable Arguments"):
        render_dataframe(
            pd.DataFrame({"All Arguments": get_exe_args(member)}),
        )

    st.write("")
    with st.expander(label="Batch and Run Settings"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Batch Settings",
            dict_name="batch_settings",
            entity=member,
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Run Settings",
            dict_name="run_settings",
            entity=member,
            df_columns=["Name", "Value"],
        )

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        build_dataframe_generic(
            column=col1,
            title="Parameters",
            dict_name="params",
            entity=member,
            df_columns=["Name", "Value"],
        )
        build_dataframe_generic(
            column=col2,
            title="Files",
            dict_name="files",
            entity=member,
            df_columns=["Type", "File"],
        )

    st.write("")
    with st.expander(label="Colocated Database"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            mem_colocated_db: t.Optional[t.Dict[str, t.Any]] = (
                member.get("colocated_db") if member is not None else {}
            )
            build_dataframe_generic(
                column=col1,
                title="Summary",
                dict_name="settings",
                entity=mem_colocated_db,
                df_columns=["Name", "Value"],
            )
            build_dataframe_loaded_entities(
                column=col2, title="Loaded Scripts and Models", entity=mem_colocated_db
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
    st.header("Experiment Overview: " + manifest.experiment.get("name", ""))
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

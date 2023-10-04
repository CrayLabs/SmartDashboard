import typing as t

import pandas as pd
import streamlit as st

from smartdashboard.utils.errors import MalformedManifestError, SSDashboardError
from smartdashboard.utils.helpers import (
    flatten_nested_keyvalue_containers,
    format_ensemble_params,
    get_db_hosts,
    get_ensemble_members,
    get_entities_with_name,
    get_exe_args,
    get_interfaces,
    get_loaded_entities,
    get_member,
    get_port,
    get_value,
)
from smartdashboard.utils.ManifestReader import Manifest
from smartdashboard.views import (
    ApplicationView,
    EnsembleView,
    ExperimentView,
    OrchestratorView,
)


def error_builder(error: SSDashboardError) -> None:
    st.header(error.title)
    st.error(
        f"""{error.body}  
         File: {error.file}"""
    )


def exp_builder(manifest: Manifest) -> ExperimentView:
    view = ExperimentView()
    st.subheader("Experiment Configuration")
    st.write("")
    col1, col2 = st.columns([4, 4])
    with col1:
        st.write("Status: :green[Running]")
        st.write("Path: " + get_value("path", manifest.experiment))
        st.write("Launcher: " + get_value("launcher", manifest.experiment))

    st.write("")
    with st.expander(label="Logs"):
        col1, col2 = st.columns([6, 6])
        with col1:
            st.write("Output")
            st.info("")

        with col2:
            st.write("Error")
            st.info("")
    return view


def app_builder(manifest: Manifest) -> ApplicationView:
    view = ApplicationView()
    st.subheader("Application Configuration")
    try:
        rendered_apps = manifest.applications
    except MalformedManifestError:
        st.error("Applications are malformed.")
        rendered_apps = []
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_app_name: t.Optional[str] = st.selectbox(
            "Select an application:",
            [app["name"] for app in rendered_apps],
        )
    if selected_app_name is not None:
        SELECTED_APPLICATION = get_entities_with_name(selected_app_name, rendered_apps)
    else:
        SELECTED_APPLICATION = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Path: " + get_value("path", SELECTED_APPLICATION))

    st.write("")
    with st.expander(label="Executable Arguments"):
        exe_arg_list = get_exe_args(SELECTED_APPLICATION)
        exe_args = {
            "All Arguments": exe_arg_list,
        }
        df = pd.DataFrame(exe_args)
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Batch and Run Settings"):
        col1, col2 = st.columns([4, 4])
        batch_settings_data = flatten_nested_keyvalue_containers(
            "batch_settings", SELECTED_APPLICATION
        )
        with col1:
            df = pd.DataFrame(batch_settings_data, columns=["Name", "Value"])
            st.write("Batch")
            st.dataframe(df, hide_index=True, use_container_width=True)
        with col2:
            run_settings_data = flatten_nested_keyvalue_containers(
                "run_settings", SELECTED_APPLICATION
            )
            df = pd.DataFrame(run_settings_data, columns=["Name", "Value"])
            st.write("Run")
            st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        with col1:
            params_data = flatten_nested_keyvalue_containers(
                "params", SELECTED_APPLICATION
            )
            df = pd.DataFrame(params_data, columns=["Name", "Value"])
            st.write("Parameters")
            st.dataframe(df, hide_index=True, use_container_width=True)
        with col2:
            file_data = flatten_nested_keyvalue_containers(
                "files", SELECTED_APPLICATION
            )
            df = pd.DataFrame(file_data, columns=["File", "Type"])
            st.write("Files")
            st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Colocated Database"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            app_colocated_db: t.Optional[t.Dict[str, t.Any]] = (
                SELECTED_APPLICATION.get("colocated_db")
                if SELECTED_APPLICATION is not None
                else {}
            )
            with col1:
                st.write("Summary")
                colo_data = flatten_nested_keyvalue_containers(
                    "settings", app_colocated_db
                )
                df = pd.DataFrame(colo_data, columns=["Name", "Value"])
                st.dataframe(df, hide_index=True, use_container_width=True)

            with col2:
                st.write("Loaded Entities")
                entities = get_loaded_entities(app_colocated_db)
                df = pd.DataFrame(entities)
                st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Logs"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            with col1:
                st.write("Output")
                st.info("")

            with col2:
                st.write("Error")
                st.info("")

    return view


def orc_builder(manifest: Manifest) -> OrchestratorView:
    view = OrchestratorView()
    st.subheader("Orchestrator Configuration")
    try:
        rendered_orcs = manifest.orchestrators
    except MalformedManifestError:
        st.error("Orchestrators are malformed.")
        rendered_orcs = []
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_orc_name: t.Optional[str] = st.selectbox(
            "Select an orchestrator:",
            [orc["name"] for orc in rendered_orcs],
        )

    if selected_orc_name is not None:
        SELECTED_ORC = get_entities_with_name(selected_orc_name, rendered_orcs)
    else:
        SELECTED_ORC = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Type: " + get_value("type", SELECTED_ORC))
    st.write("Port: " + get_port(SELECTED_ORC))
    st.write("Interface: " + get_interfaces(SELECTED_ORC))

    st.write("")
    with st.expander(label="Database Hosts"):
        hosts = {
            "Hosts": get_db_hosts(SELECTED_ORC),
        }
        df = pd.DataFrame(hosts)
        st.dataframe(df, hide_index=True, use_container_width=True)
    st.write("")
    with st.expander(label="Logs"):
        col1, col2 = st.columns([6, 6])
        with col1:
            st.session_state["shard_name"] = st.selectbox(
                label="Shard", options=("Shard 1", "Shard 2", "Shard 3", "Shard 4")
            )
            st.write("")
            st.write("Output")
            st.info("")

        with col2:
            st.write("#")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("Error")
            st.info("")

    return view


def ens_builder(manifest: Manifest) -> EnsembleView:
    view = EnsembleView()
    st.subheader("Ensemble Configuration")
    try:
        rendered_ensembles = manifest.ensembles
    except MalformedManifestError:
        st.error("Ensembles are malformed.")
        rendered_ensembles = []
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_ensemble_name: t.Optional[str] = st.selectbox(
            "Select an ensemble:",
            [ensemble["name"] for ensemble in rendered_ensembles],
        )

    if selected_ensemble_name is not None:
        SELECTED_ENSEMBLE = get_entities_with_name(
            selected_ensemble_name, rendered_ensembles
        )
    else:
        SELECTED_ENSEMBLE = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Strategy: " + get_value("perm_strat", SELECTED_ENSEMBLE))

    st.write("")
    with st.expander(label="Batch Settings"):
        ens_batch_data = flatten_nested_keyvalue_containers(
            "batch_settings", SELECTED_ENSEMBLE
        )
        df = pd.DataFrame(ens_batch_data, columns=["Name", "Value"])
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Parameters"):
        ens_param_data = format_ensemble_params(SELECTED_ENSEMBLE)
        df = pd.DataFrame(ens_param_data, columns=["Name", "Value"])
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("#")
    if selected_ensemble_name is not None:
        st.subheader(selected_ensemble_name + " Member Configuration")
    else:
        st.subheader("Member Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        members = get_ensemble_members(SELECTED_ENSEMBLE)
        selected_member_name: t.Optional[str] = st.selectbox(
            "Select a member:",
            [member["name"] for member in members if member],
        )

    if selected_member_name is not None:
        SELECTED_MEMBER = get_member(selected_member_name, SELECTED_ENSEMBLE)
    else:
        SELECTED_MEMBER = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Path: " + get_value("path", SELECTED_MEMBER))
    st.write("")
    with st.expander(label="Executable Arguments"):
        args = get_exe_args(SELECTED_MEMBER)
        exe_args = {"All Arguments": args}
        df = pd.DataFrame(exe_args)
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Batch and Run Settings"):
        col1, col2 = st.columns([4, 4])
        with col1:
            mem_batch_data = flatten_nested_keyvalue_containers(
                "batch_settings", SELECTED_MEMBER
            )
            df = pd.DataFrame(mem_batch_data, columns=["Name", "Value"])
            st.write("Batch")
            st.dataframe(df, hide_index=True, use_container_width=True)
        with col2:
            mem_run_data = flatten_nested_keyvalue_containers(
                "run_settings", SELECTED_MEMBER
            )
            df = pd.DataFrame(mem_run_data, columns=["Name", "Value"])
            st.write("Run")
            st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        with col1:
            mem_param_data = flatten_nested_keyvalue_containers(
                "params", SELECTED_MEMBER
            )
            df = pd.DataFrame(mem_param_data, columns=["Name", "Value"])
            st.write("Parameters")
            st.dataframe(df, hide_index=True, use_container_width=True)
        with col2:
            mem_file_data = flatten_nested_keyvalue_containers("files", SELECTED_MEMBER)
            df = pd.DataFrame(mem_file_data, columns=["Type", "File"])
            st.write("Files")
            st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Colocated Database"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            mem_colocated_db: t.Optional[t.Dict[str, t.Any]] = (
                SELECTED_MEMBER.get("colocated_db")
                if SELECTED_MEMBER is not None
                else {}
            )
            with col1:
                st.write("Summary")
                mem_colo_data = flatten_nested_keyvalue_containers(
                    "settings", mem_colocated_db
                )
                df = pd.DataFrame(mem_colo_data, columns=["Name", "Value"])
                st.dataframe(df, hide_index=True, use_container_width=True)

            with col2:
                st.write("Loaded Entities")
                mem_entities = get_loaded_entities(mem_colocated_db)
                df = pd.DataFrame(mem_entities)
                st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Logs"):
        col1, col2 = st.columns([6, 6])
        with col1:
            st.write("Output")
            st.info("")

        with col2:
            st.write("Error")
            st.info("")

    return view

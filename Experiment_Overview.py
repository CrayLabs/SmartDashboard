import pandas as pd
import streamlit as st
import typing as t
from utils.pageSetup import (
    local_css,
    set_streamlit_page_config,
)
from utils.FileReader import ManifestReader
from utils.helpers import (
    get_db_hosts,
    get_port,
    format_ensemble_params,
    format_mixed_nested_dict,
    get_exe_args,
    get_value,
    get_interface,
    get_loaded_entities,
    get_ensemble_members,
    get_member,
    get_entities_with_name,
)

set_streamlit_page_config()
local_css("assets/style.scss")

# get real path and manifest.json
manifest = ManifestReader.from_file("tests/test_utils/manifest_files/no_apps_manifest.json")


if manifest.experiment == {}:
    st.header("Experiment Not Found")
else:
    st.header("Experiment Overview: " + get_value("name", manifest.experiment))

st.write("")

experiment, application, orchestrators, ensembles = st.tabs(
    ["Experiment", "Applications", "Orchestrators", "Ensembles"]
)

### Experiment ###
with experiment:
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

### Applications ###
with application:
    st.subheader("Application Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_app_name: t.Optional[str] = st.selectbox(
            "Select an application:",
            [app["name"] for app in manifest.applications],
        )
    if selected_app_name is not None:
        SELECTED_APPLICATION = get_entities_with_name(
            selected_app_name, manifest.applications
        )
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
        batch_names, batch_values = format_mixed_nested_dict(
            "batch_settings", SELECTED_APPLICATION
        )
        with col1:
            batch = {"Name": batch_names, "Value": batch_values}
            df = pd.DataFrame(batch)
            st.write("Batch")
            st.dataframe(df, hide_index=True, use_container_width=True)
        with col2:
            run_names, run_values = format_mixed_nested_dict(
                "run_settings", SELECTED_APPLICATION
            )
            rs = {"Name": run_names, "Value": run_values}
            df = pd.DataFrame(rs)
            st.write("Run")
            st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        with col1:
            (
                param_names,
                param_values,
            ) = format_mixed_nested_dict("params", SELECTED_APPLICATION)
            params = {
                "Name": param_names,
                "Value": param_values,
            }
            df = pd.DataFrame(params)
            st.write("Parameters")
            st.dataframe(df, hide_index=True, use_container_width=True)
        with col2:
            file_type, file_paths = format_mixed_nested_dict(
                "files", SELECTED_APPLICATION
            )
            files = {
                "File": file_paths,
                "Type": file_type,
            }
            df = pd.DataFrame(files)
            st.write("Files")
            st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Colocated Database"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            app_colocated_db: t.Optional[t.Dict[str, t.Any]] = get_value(
                "colocated_db", SELECTED_APPLICATION
            )
            with col1:
                st.write("Summary")
                colo_keys, colo_vals = format_mixed_nested_dict(
                    "settings", app_colocated_db
                )
                colo_db = {"Name": colo_keys, "Value": colo_vals}
                df = pd.DataFrame(colo_db)
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

### Orchestrator ###
with orchestrators:
    st.subheader("Orchestrator Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_orc_name: t.Optional[str] = st.selectbox(
            "Select an orchestrator:",
            [orc["name"] for orc in manifest.orchestrators],
        )

    if selected_orc_name is not None:
        SELECTED_ORC = get_entities_with_name(selected_orc_name, manifest.orchestrators)
    else:
        SELECTED_ORC = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Type: " + get_value("type", SELECTED_ORC))
    st.write("Port: " + get_port(SELECTED_ORC))
    st.write("Interface: " + get_interface(SELECTED_ORC))

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
            out = st.empty()
            st.info("")

        with col2:
            st.write("#")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("Error")
            err = st.empty()
            st.info("")

### Ensembles ###
with ensembles:
    st.subheader("Ensemble Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_ensemble_name: t.Optional[str] = st.selectbox(
            "Select an ensemble:",
            [ensemble["name"] for ensemble in manifest.ensembles],
        )

    if selected_ensemble_name is not None:
        SELECTED_ENSEMBLE = get_entities_with_name(
            selected_ensemble_name, manifest.ensembles
        )
    else:
        SELECTED_ENSEMBLE = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Strategy: " + get_value("perm_strat", SELECTED_ENSEMBLE))

    st.write("")
    with st.expander(label="Batch Settings"):
        batch_names, batch_values = format_mixed_nested_dict(
            "batch_settings", SELECTED_ENSEMBLE
        )
        batch = {
            "Name": batch_names,
            "Value": batch_values,
        }
        df = pd.DataFrame(batch)
        st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Parameters"):
        (
            ens_param_names,
            ens_param_values,
        ) = format_ensemble_params(SELECTED_ENSEMBLE)
        ens_params = {
            "Name": ens_param_names,
            "Value": ens_param_values,
        }
        df = pd.DataFrame(ens_params)
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
            [member["name"] for member in members if member is not None],
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
            (
                mem_batch_name,
                mem_batch_value,
            ) = format_mixed_nested_dict("batch_settings", SELECTED_MEMBER)
            batch = {
                "Name": mem_batch_name,
                "Value": mem_batch_value,
            }
            df = pd.DataFrame(batch)
            st.write("Batch")
            st.dataframe(df, hide_index=True, use_container_width=True)
        with col2:
            mem_rs_name, mem_rs_value = format_mixed_nested_dict(
                "run_settings", SELECTED_MEMBER
            )
            rs = {
                "Name": mem_rs_name,
                "Value": mem_rs_value,
            }
            df = pd.DataFrame(rs)
            st.write("Run")
            st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        with col1:
            (
                mem_param_name,
                mem_param_value,
            ) = format_mixed_nested_dict("params", SELECTED_MEMBER)
            params = {
                "Name": mem_param_name,
                "Value": mem_param_value,
            }
            df = pd.DataFrame(params)
            st.write("Parameters")
            st.dataframe(df, hide_index=True, use_container_width=True)
        with col2:
            mem_file_type, mem_files = format_mixed_nested_dict(
                "files", SELECTED_MEMBER
            )
            files = {
                "File": mem_files,
                "Type": mem_file_type,
            }
            df = pd.DataFrame(files)
            st.write("Files")
            st.dataframe(df, hide_index=True, use_container_width=True)

    st.write("")
    with st.expander(label="Colocated Database"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            mem_colocated_db: t.Optional[t.Dict[str, t.Any]] = get_value(
                "colocated_db", SELECTED_MEMBER
            )
            with col1:
                st.write("Summary")
                (
                    mem_colo_keys,
                    mem_colo_vals,
                ) = format_mixed_nested_dict("settings", mem_colocated_db)
                mem_colo_db = {"Name": mem_colo_keys, "Value": mem_colo_vals}
                df = pd.DataFrame(mem_colo_db)
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

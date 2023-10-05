import traceback
import typing as t

import pandas as pd
import streamlit as st

from smartdashboard.utils.errors import SSDashboardError
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
    """Error view displayed when errors are caught

    :param error: Error to get information from
    :type error: SSDashboardError
    """
    st.header(error.title)
    st.error(
        f"""Error found in file: {error.file}  
             Error Message: {error.exception}"""
    )

    with st.expander(label="Traceback"):
        st.code(traceback.format_exc(), language="python")


def exp_builder(manifest: Manifest) -> ExperimentView:
    """Experiment view to be rendered

    :param manifest: Manifest to get dashboard info from
    :type manifest: Manifest
    :return: An experiment view
    :rtype: ExperimentView
    """
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
    """Application view to be rendered

    :param manifest: Manifest to get dashboard info from
    :type manifest: Manifest
    :return: An application view
    :rtype: ApplicationView
    """
    view = ApplicationView()
    st.subheader("Application Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_app_name: t.Optional[str] = st.selectbox(
            "Select an application:",
            [app["name"] for app in manifest.applications],
        )
    if selected_app_name is not None:
        selected_application = get_entities_with_name(
            selected_app_name, manifest.applications
        )
    else:
        selected_application = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Path: " + get_value("path", selected_application))

    st.write("")
    with st.expander(label="Executable Arguments"):
        st.dataframe(
            pd.DataFrame(
                {
                    "All Arguments": get_exe_args(selected_application),
                }
            ),
            hide_index=True,
            use_container_width=True,
        )

    st.write("")
    with st.expander(label="Batch and Run Settings"):
        col1, col2 = st.columns([4, 4])
        with col1:
            st.write("Batch")
            st.dataframe(
                pd.DataFrame(
                    flatten_nested_keyvalue_containers(
                        "batch_settings", selected_application
                    ),
                    columns=["Name", "Value"],
                ),
                hide_index=True,
                use_container_width=True,
            )
        with col2:
            st.write("Run")
            st.dataframe(
                pd.DataFrame(
                    flatten_nested_keyvalue_containers(
                        "run_settings", selected_application
                    ),
                    columns=["Name", "Value"],
                ),
                hide_index=True,
                use_container_width=True,
            )

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        with col1:
            st.write("Parameters")
            st.dataframe(
                pd.DataFrame(
                    flatten_nested_keyvalue_containers("params", selected_application),
                    columns=["Name", "Value"],
                ),
                hide_index=True,
                use_container_width=True,
            )
        with col2:
            st.write("Files")
            st.dataframe(
                pd.DataFrame(
                    flatten_nested_keyvalue_containers("files", selected_application),
                    columns=["Type", "File"],
                ),
                hide_index=True,
                use_container_width=True,
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
            with col1:
                st.write("Summary")
                st.dataframe(
                    pd.DataFrame(
                        flatten_nested_keyvalue_containers(
                            "settings", app_colocated_db
                        ),
                        columns=["Name", "Value"],
                    ),
                    hide_index=True,
                    use_container_width=True,
                )

            with col2:
                st.write("Loaded Entities")
                st.dataframe(
                    pd.DataFrame(get_loaded_entities(app_colocated_db)),
                    hide_index=True,
                    use_container_width=True,
                )

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
    """Orchestrator view to be rendered

    :param manifest: Manifest to get dashboard info from
    :type manifest: Manifest
    :return: An orchestrator view
    :rtype: OrchestratorView
    """
    view = OrchestratorView()
    st.subheader("Orchestrator Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_orc_name: t.Optional[str] = st.selectbox(
            "Select an orchestrator:",
            [orc["name"] for orc in manifest.orchestrators],
        )

    if selected_orc_name is not None:
        selected_orc = get_entities_with_name(selected_orc_name, manifest.orchestrators)
    else:
        selected_orc = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Type: " + get_value("type", selected_orc))
    st.write("Port: " + get_port(selected_orc))
    st.write("Interface: " + get_interfaces(selected_orc))

    st.write("")
    with st.expander(label="Database Hosts"):
        st.dataframe(
            pd.DataFrame(
                {
                    "Hosts": get_db_hosts(selected_orc),
                }
            ),
            hide_index=True,
            use_container_width=True,
        )
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
    """Ensemble view to be rendered

    :param manifest: Manifest to get dashboard info from
    :type manifest: Manifest
    :return: An ensemble view
    :rtype: EnsembleView
    """
    view = EnsembleView()
    st.subheader("Ensemble Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        selected_ensemble_name: t.Optional[str] = st.selectbox(
            "Select an ensemble:",
            [ensemble["name"] for ensemble in manifest.ensembles],
        )

    if selected_ensemble_name is not None:
        selected_ensemble = get_entities_with_name(
            selected_ensemble_name, manifest.ensembles
        )
    else:
        selected_ensemble = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Strategy: " + get_value("perm_strat", selected_ensemble))

    st.write("")
    with st.expander(label="Batch Settings"):
        st.dataframe(
            pd.DataFrame(
                flatten_nested_keyvalue_containers("batch_settings", selected_ensemble),
                columns=["Name", "Value"],
            ),
            hide_index=True,
            use_container_width=True,
        )

    st.write("")
    with st.expander(label="Parameters"):
        st.dataframe(
            pd.DataFrame(
                format_ensemble_params(selected_ensemble), columns=["Name", "Value"]
            ),
            hide_index=True,
            use_container_width=True,
        )

    st.write("#")
    if selected_ensemble_name is not None:
        st.subheader(selected_ensemble_name + " Member Configuration")
    else:
        st.subheader("Member Configuration")
    col1, col2 = st.columns([4, 4])
    with col1:
        members = get_ensemble_members(selected_ensemble)
        selected_member_name: t.Optional[str] = st.selectbox(
            "Select a member:",
            [member["name"] for member in members if member],
        )

    if selected_member_name is not None:
        selected_member = get_member(selected_member_name, selected_ensemble)
    else:
        selected_member = None

    st.write("")
    st.write("Status: :green[Running]")
    st.write("Path: " + get_value("path", selected_member))
    st.write("")
    with st.expander(label="Executable Arguments"):
        st.dataframe(
            pd.DataFrame({"All Arguments": get_exe_args(selected_member)}),
            hide_index=True,
            use_container_width=True,
        )

    st.write("")
    with st.expander(label="Batch and Run Settings"):
        col1, col2 = st.columns([4, 4])
        with col1:
            st.write("Batch")
            st.dataframe(
                pd.DataFrame(
                    flatten_nested_keyvalue_containers(
                        "batch_settings", selected_member
                    ),
                    columns=["Name", "Value"],
                ),
                hide_index=True,
                use_container_width=True,
            )
        with col2:
            st.write("Run")
            st.dataframe(
                pd.DataFrame(
                    flatten_nested_keyvalue_containers("run_settings", selected_member),
                    columns=["Name", "Value"],
                ),
                hide_index=True,
                use_container_width=True,
            )

    st.write("")
    with st.expander(label="Parameters and Generator Files"):
        col1, col2 = st.columns([4, 4])
        with col1:
            st.write("Parameters")
            st.dataframe(
                pd.DataFrame(
                    flatten_nested_keyvalue_containers("params", selected_member),
                    columns=["Name", "Value"],
                ),
                hide_index=True,
                use_container_width=True,
            )
        with col2:
            st.write("Files")
            st.dataframe(
                pd.DataFrame(
                    flatten_nested_keyvalue_containers("files", selected_member),
                    columns=["Type", "File"],
                ),
                hide_index=True,
                use_container_width=True,
            )

    st.write("")
    with st.expander(label="Colocated Database"):
        with st.container():
            col1, col2 = st.columns([6, 6])
            mem_colocated_db: t.Optional[t.Dict[str, t.Any]] = (
                selected_member.get("colocated_db")
                if selected_member is not None
                else {}
            )
            with col1:
                st.write("Summary")
                st.dataframe(
                    pd.DataFrame(
                        flatten_nested_keyvalue_containers(
                            "settings", mem_colocated_db
                        ),
                        columns=["Name", "Value"],
                    ),
                    hide_index=True,
                    use_container_width=True,
                )

            with col2:
                st.write("Loaded Entities")
                st.dataframe(
                    pd.DataFrame(get_loaded_entities(mem_colocated_db)),
                    hide_index=True,
                    use_container_width=True,
                )

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

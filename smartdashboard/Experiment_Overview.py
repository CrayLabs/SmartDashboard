import os
import pathlib

import streamlit as st

from smartdashboard.builders import (
    app_builder,
    ens_builder,
    error_builder,
    exp_builder,
    orc_builder,
)
from smartdashboard.utils.errors import SSDashboardError
from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.ManifestReader import load_manifest
from smartdashboard.utils.pageSetup import local_css, set_streamlit_page_config

set_streamlit_page_config()

curr_path = pathlib.Path(os.path.abspath(__file__)).parent
local_css(str(curr_path / "static/style.css"))


try:
    manifest = load_manifest("tests/test_utils/manifest_files/no_apps_manifest.json")
except SSDashboardError as ss:
    error_builder(ss)
    manifest = None


if manifest:
    st.header("Experiment Overview: " + get_value("name", manifest.experiment))

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

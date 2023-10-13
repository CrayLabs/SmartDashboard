import os
import pathlib

import streamlit as st

from smartdashboard.utils.errors import SSDashboardError
from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.ManifestReader import load_manifest
from smartdashboard.utils.pageSetup import local_css, set_streamlit_page_config
from smartdashboard.view_builders import (
    app_builder,
    ens_builder,
    error_builder,
    exp_builder,
    orc_builder,
)

set_streamlit_page_config()

curr_path = pathlib.Path(os.path.abspath(__file__)).parent
local_css(curr_path / "static/style.css")


try:
    MANIFEST = load_manifest("tests/utils/manifest_files/manifesttest.json")
except SSDashboardError as ss:
    error_builder(ss)
else:
    st.header("Experiment Overview: " + get_value("name", MANIFEST.experiment))

    st.write("")

    experiment, application, orchestrators, ensembles = st.tabs(
        ["Experiment", "Applications", "Orchestrators", "Ensembles"]
    )

    ### Experiment ###
    with experiment:
        exp_view = exp_builder(MANIFEST)

    ### Applications ###
    with application:
        app_view = app_builder(MANIFEST)

    ### Orchestrator ###
    with orchestrators:
        orc_view = orc_builder(MANIFEST)

    ### Ensembles ###
    with ensembles:
        ens_view = ens_builder(MANIFEST)

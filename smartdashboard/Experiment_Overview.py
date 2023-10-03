import os
import pathlib

import streamlit as st

from smartdashboard.builders import *
from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.ManifestReader import ManifestFileReader
from smartdashboard.utils.pageSetup import local_css, set_streamlit_page_config

set_streamlit_page_config()

curr_path = pathlib.Path(os.path.abspath(__file__)).parent
local_css(str(curr_path / "static/style.css"))

# get real path and manifest.json
manifest_file_reader = ManifestFileReader(
    "tests/test_utils/manifest_files/no_experiment_manifest.json"
)
manifest = manifest_file_reader.get_manifest()

st.header("Experiment Overview: " + get_value("name", manifest.experiment))

st.write("")

experiment, application, orchestrators, ensembles = st.tabs(
    ["Experiment", "Applications", "Orchestrators", "Ensembles"]
)

### Experiment ###
with experiment:
    exp_builder(manifest)

### Applications ###
with application:
    app_builder(manifest)

### Orchestrator ###
with orchestrators:
    orc_builder(manifest)

### Ensembles ###
with ensembles:
    ens_builder(manifest)

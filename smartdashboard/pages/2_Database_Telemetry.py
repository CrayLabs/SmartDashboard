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

import os
import pathlib
import sys
import time

import streamlit as st

from smartdashboard.utils.errors import SSDashboardError
from smartdashboard.utils.ManifestReader import get_manifest_path, load_manifest
from smartdashboard.utils.pageSetup import local_css, set_streamlit_page_config
from smartdashboard.view_builders import db_telem_builder, error_builder


def build_telemetry_page() -> None:
    """Build the application components with streamlit
    for the Database Telemetry page
    """
    set_streamlit_page_config()

    curr_path = pathlib.Path(os.path.abspath(__file__)).parent.parent
    local_css(str(curr_path / "static/style.css"))

    if "manifest" not in st.session_state:
        manifest_path = get_manifest_path(
            sys.argv[1:], pathlib.Path(__file__).parent.parent.parent
        )
        try:
            manifest = load_manifest(manifest_path)
            st.session_state["manifest"] = manifest
        except SSDashboardError as ex:
            error_builder(ex)
            return

    update_telemetry_page()


def update_telemetry_page() -> None:
    """Update the components for the Database Telemetry page"""
    views = db_telem_builder(st.session_state["manifest"])

    while True:
        for v in [views.orc_summary_view, views.memory_view, views.client_view]:
            v.update()

        time.sleep(1)


if __name__ == "__main__":
    build_telemetry_page()

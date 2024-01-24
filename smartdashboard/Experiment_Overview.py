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

import os
import pathlib
import sys
import time
import typing as t
from subprocess import run

import streamlit as st

from smartdashboard.utils.argparser import get_parser
from smartdashboard.utils.errors import SSDashboardError
from smartdashboard.utils.ManifestReader import get_manifest_path, load_manifest
from smartdashboard.utils.pageSetup import local_css, set_streamlit_page_config
from smartdashboard.view_builders import error_builder, overview_builder
from smartdashboard.views import EntityView


def build_app(manifest_path: str) -> None:
    """Build the application components with streamlit

    :param manifest_path: Path to build Manifest with
    :type manifest_path: str
    """
    set_streamlit_page_config()

    curr_path = pathlib.Path(os.path.abspath(__file__)).parent
    local_css(str(curr_path / "static/style.css"))

    try:
        manifest = load_manifest(manifest_path)
        st.session_state["manifest"] = manifest
    except SSDashboardError as ex:
        error_builder(ex)
    else:
        views = overview_builder(manifest)
        to_update: t.Iterable[EntityView[t.Any]] = (
            views.exp_view,
            views.app_view,
            views.orc_view,
            views.ens_view,
        )

        while True:
            for v in to_update:
                v.update()

            time.sleep(1)


def run_dash_app(exp_path: str, app_port: int) -> None:
    """Execute the dashboard app by invoking streamlit

    :param exp_path: Path to experiment directory
    :type exp_path: str
    :param app_port: Port that the application is launched on
    :type app_port: int
    """
    app_cmd = [
        "streamlit",
        "run",
        os.path.abspath(__file__),
        "--server.port",
        str(app_port),
        "--server.enableStaticServing",
        "1",
        "--theme.base",
        "dark",
        "--theme.primaryColor",
        "#17eba0",
        "--",
        "-d",
        exp_path,
    ]
    run(app_cmd, check=False)
    sys.exit(0)


def cli() -> None:
    """Execute the dashboard app by invoking streamlit"""
    arg_parser = get_parser()
    args = arg_parser.parse_args(sys.argv[1:])

    exp_path = pathlib.Path(os.getcwd())

    if args.directory is not None:
        exp_path = pathlib.Path(args.directory)

    app_port: int = args.port

    run_dash_app(str(exp_path), app_port)


if __name__ == "__main__":
    # sample direct execution:
    # streamlit run ./smartdashboard/Experiment_Overview.py --
    #       -d <repo_path>/tests/utils/manifest_files/fauxexp
    PATH = get_manifest_path(sys.argv[1:], pathlib.Path(__file__).parent.parent)
    build_app(PATH)

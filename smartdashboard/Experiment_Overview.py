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
from subprocess import run

import streamlit as st

from smartdashboard.utils.argparser import get_parser
from smartdashboard.utils.errors import SSDashboardError
from smartdashboard.utils.ManifestReader import create_filereader, get_manifest_path
from smartdashboard.utils.pageSetup import local_css, set_streamlit_page_config
from smartdashboard.view_builders import error_builder, overview_builder


def build_app(manifest_path: pathlib.Path) -> None:
    """Build the application components with streamlit

    :param manifest_path: Path to build Manifest with
    :type manifest_path: pathlib.Path
    """
    set_streamlit_page_config()

    curr_path = pathlib.Path(os.path.abspath(__file__)).parent
    local_css(str(curr_path / "static/style.css"))

    try:
        manifest_reader = create_filereader(manifest_path)
        manifest = manifest_reader.get_manifest()
        st.session_state["manifest"] = manifest
    except SSDashboardError as ex:
        error_builder(ex)
    else:
        views = overview_builder(manifest)

        while True:
            if manifest_reader.has_changed:
                st.rerun()
            views.update()
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
    cli_args = get_parser().parse_args(sys.argv[1:])
    directory = (
        pathlib.Path(cli_args.directory) if cli_args.directory is not None else None
    )
    PATH = get_manifest_path(directory)
    build_app(PATH)

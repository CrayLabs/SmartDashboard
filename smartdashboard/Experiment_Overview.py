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

import argparse
import os
import pathlib
import sys
import time
import typing as t
from subprocess import run

from smartdashboard.views import EntityView
from smartdashboard.utils.errors import SSDashboardError
from smartdashboard.utils.ManifestReader import load_manifest
from smartdashboard.utils.pageSetup import local_css, set_streamlit_page_config
from smartdashboard.view_builders import error_builder, overview_builder


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
    except SSDashboardError as ex:
        error_builder(ex)
    else:
        views = overview_builder(manifest)

        while True:
            for v in [views.exp_view, views.app_view, views.orc_view, views.ens_view]:
                if isinstance(v, EntityView):
                    v.update()

            time.sleep(1)


def get_parser() -> argparse.ArgumentParser:
    """Build an argument parser to handle the expected CLI arguments

    :return: Argument parser that handles CLI arguments
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser("smart-dash", prefix_chars="-")
    parser.add_argument(
        "-d",
        "--directory",
        help="The path to an experiment to load. Default to current directory",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-p",
        "--port",
        help="The port to expose the dashboard on",
        type=int,
        default=8501,
    )
    return parser


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


def execute(args: t.List[str]) -> None:
    """Build the dashboard application

    :param args: Passed in arguments
    :type args: List[str]
    """
    arg_parser = get_parser()
    parsed_args: argparse.Namespace = arg_parser.parse_args(args)

    # default behavior will load a demo manifest from the test samples
    exp_path = pathlib.Path(__file__).parent.parent
    manifest_path = exp_path / "tests/utils/manifest_files/manifesttest.json"
    if parsed_args.directory is not None:
        exp_path = pathlib.Path(parsed_args.directory)
        manifest_path = exp_path / ".smartsim/telemetry/manifest.json"

    build_app(str(manifest_path))


if __name__ == "__main__":
    # sample direct execution:
    # streamlit run ./smartdashboard/Experiment_Overview.py --
    #       -d <repo_path>/tests/utils/manifest_files/fauxexp
    execute(sys.argv[1:])

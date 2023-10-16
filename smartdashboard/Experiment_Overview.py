import argparse
import os
import pathlib
import sys
import typing as t

from subprocess import run

from smartdashboard.utils.errors import SSDashboardError
from smartdashboard.utils.ManifestReader import load_manifest
from smartdashboard.utils.pageSetup import local_css, set_streamlit_page_config
from smartdashboard.view_builders import overview_builder, error_builder


def build_app(manifest_path: str) -> None:
    """Build the application components with streamlit"""
    set_streamlit_page_config()

    curr_path = pathlib.Path(os.path.abspath(__file__)).parent
    local_css(str(curr_path / "static/style.css"))

    try:
        manifest = load_manifest(manifest_path)
    except SSDashboardError as ss:
        error_builder(ss)
    else:
        overview_builder(manifest)


def get_parser() -> argparse.ArgumentParser:
    """Build an argument parser to handle the expected CLI arguments"""
    parser = argparse.ArgumentParser("smart-dash", prefix_chars="-")
    parser.add_argument(
        "-d",
        help="The path to an experiment to load. Default to current directory",
        type=str,
        default=None,
    )
    parser.add_argument(
        "-p",
        help="The port to expose the dashboard on",
        type=int,
        default=8501,
    )
    return parser


def run_dash_app(exp_path: str, app_port: int) -> None:
    """Execute the dashboard app by invoking streamlit"""
    app_cmd = [
        "streamlit",
        "run",
        os.path.abspath(__file__),
        "--browser.serverPort",
        str(app_port),
        "--server.port",
        str(app_port),
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

    if args.d is not None:
        exp_path = pathlib.Path(args.d)

    app_port: int = args.p

    run_dash_app(str(exp_path), app_port)


def execute(args: t.List[str]) -> None:
    """Build the dashboard application"""
    arg_parser = get_parser()
    parsed_args: argparse.Namespace = arg_parser.parse_args(args)

    # default behavior will load a demo manifest from the test samples
    exp_path = pathlib.Path(__file__).parent.parent
    manifest_path = exp_path / "tests/utils/manifest_files/manifesttest.json"
    if parsed_args.d is not None:
        exp_path = pathlib.Path(parsed_args.d)
        manifest_path = exp_path / ".smartsim/telemetry/manifest.json"

    build_app(str(manifest_path))


if __name__ == "__main__":
    # sample direct execution:
    # streamlit run ./smartdashboard/Experiment_Overview.py --
    #       -d <repo_path>/tests/utils/manifest_files/fauxexp
    execute(sys.argv[1:])

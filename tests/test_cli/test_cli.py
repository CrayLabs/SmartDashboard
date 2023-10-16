import pytest
import sys

from smartdashboard import Experiment_Overview as expo


def test_cli_args_port():
    """ensure the short & long parameter versions are parsed"""
    exp_port = 1234
    param_str = f"-p {exp_port}".split(" ")
    parser = expo.get_parser()
    args = parser.parse_args(param_str)
    
    assert args.port
    assert args.port == exp_port

    param_str = f"--port {exp_port}".split(" ")
    parser = expo.get_parser()
    args = parser.parse_args(param_str)
    
    assert args.port
    assert args.port == exp_port

def test_cli_args_dir():
    """ensure the short & long parameter versions are parsed"""
    exp_dir = "/foo/bar/baz"
    param_str = f"-d {exp_dir}".split(" ")
    parser = expo.get_parser()
    args = parser.parse_args(param_str)
    
    assert args.dir
    assert args.dir == exp_dir

    param_str = f"--dir {exp_dir}".split(" ")
    parser = expo.get_parser()
    args = parser.parse_args(param_str)
    
    assert args.dir
    assert args.dir == exp_dir


def test_cli_args_all():
    """ensure all parameters are parsed"""
    exp_port = 1234
    exp_dir = "/foo/bar/baz"
    param_str = f"-p {exp_port} --dir {exp_dir}".split(" ")
    parser = expo.get_parser()
    args = parser.parse_args(param_str)
    
    assert args.port == exp_port
    assert args.dir == exp_dir

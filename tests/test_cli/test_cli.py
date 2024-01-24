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

    assert args.directory
    assert args.directory == exp_dir

    param_str = f"--directory {exp_dir}".split(" ")
    parser = expo.get_parser()
    args = parser.parse_args(param_str)

    assert args.directory
    assert args.directory == exp_dir


def test_cli_args_all():
    """ensure all parameters are parsed"""
    exp_port = 1234
    exp_dir = "/foo/bar/baz"
    param_str = f"-p {exp_port} --directory {exp_dir}".split(" ")
    parser = expo.get_parser()
    args = parser.parse_args(param_str)

    assert args.port == exp_port
    assert args.directory == exp_dir

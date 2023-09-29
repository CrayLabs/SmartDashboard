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

# Welcome to the SmartSim setup.py
#
# The following environment variables represent build time
# options for SmartSim. These are only relevant to when a user
# or CI is invoking the setup.py script.
#
#
# NO_CHECKS
#   If set to 1, the build process will not check for
#   build dependencies like make, gcc, etc
#
# SMARTSIM_REDIS
#   The version of redis to retrive and build with
#
# SMARTSIM_REDIS_URL
#   The URL from which to retrieve redis source code
#
# SMARTREDIS_VERSION
#   The version of SmartRedis to install.
#
# CC
#   The C compiler to use
#
# CXX
#   the CPP compiler to use
#
# MALLOC
#   The memory allocator to use for Redis (options: libc, jemalloc)
#
# BUILD_JOBS
#   Number of jobs to use in the build (defaults to max on node)
#
# SMARTSIM_SUFFIX
#  if set, the version number is set to a developer build
#  with the current version, git-sha, and suffix. This version
#  is then written into SmartSim/smartsim/version.py
#
#
# This future is needed to print Python2 EOL message
from __future__ import print_function
import sys

if sys.version_info < (3,):
    print("Python 2 has reached end-of-life and is not supported by SmartDashboard")
    sys.exit(-1)


import os
import importlib.util
from pathlib import Path

from setuptools import setup
from setuptools.dist import Distribution
from setuptools.command.install import install
from setuptools.command.build_py import build_py

# # Some necessary evils we have to do to be able to use
# # the _install tools in smartsim/smartsim/_core/_install
# # in both the setup.py and in the smart cli

# # import the installer classes
# setup_path = Path(os.path.abspath(os.path.dirname(__file__)))
# _install_dir = setup_path.joinpath("smartdashboard/_core/_install")

# # import buildenv module
# buildenv_path = _install_dir.joinpath("buildenv.py")
# buildenv_spec = importlib.util.spec_from_file_location("buildenv", str(buildenv_path))
# buildenv = importlib.util.module_from_spec(buildenv_spec)
# buildenv_spec.loader.exec_module(buildenv)

# # import builder module
# builder_path = _install_dir.joinpath("builder.py")
# builder_spec = importlib.util.spec_from_file_location("builder", str(builder_path))
# builder = importlib.util.module_from_spec(builder_spec)
# builder_spec.loader.exec_module(builder)

# # helper classes for building dependencies that are
# # also utilized by the Smart CLI
# build_env = buildenv.BuildEnv(checks=False)
# versions = buildenv.Versioner()

# # check for compatible python versions
# if not build_env.is_compatible_python(versions.PYTHON_MIN):
#     print("You are using Python {}. Python >={} is required.".format(build_env.python_version,
#                                                                      ".".join((versions.PYTHON_MIN))))
#     sys.exit(-1)

# if build_env.is_windows():
#     print("Windows is not supported by SmartSim")
#     sys.exit(-1)

# write the SmartSim version into
# smartsim/version.py and to be set as
# __version__ in smartsim/__init__.py
# smartsim_version = versions.write_version(setup_path)

# Tested with wheel v0.29.0
class BinaryDistribution(Distribution):
    """Distribution which always forces a binary package with platform name

       We use this because we want to pre-package Redis for certain
       platforms to use.
    """
    def has_ext_modules(_placeholder):
        return True


# Define needed dependencies for the installation
deps = [
    "pandas>=2.1.1",
    "streamlit>=1.27.1",
]

# Add SmartRedis at specific version
# deps.append("smartredis>={}".format(versions.SMARTREDIS))

extras_require = {
    "dev": [
        "black>=20.8b1",
        "isort>=5.6.4",
        "pylint>=2.10.0",
        "pytest>=6.0.0",
        "pytest-cov>=2.10.1",
    ],
    "mypy": [
        "mypy>=1.3.0",
        "pandas-stubs",
        "types-Pillow",
    ],
}


# rest in setup.cfg
setup(
    version="0.0.1",  # smartsim_version,
    install_requires=deps,
    packages=["smartdashboard"],
    package_data={"smartdashboard": [
        "bin/*",
    ]},
    zip_safe=False,
    extras_require=extras_require,
    distclass=BinaryDistribution,
    entry_points={
        "console_scripts": [
            "smart-dash = smartdashboard._cli.__main__:main",
        ]
    }
)

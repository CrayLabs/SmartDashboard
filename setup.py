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

# Welcome to the SmartDashboard setup.py

# This future is needed to print Python2 EOL message
from __future__ import print_function
import sys

if sys.version_info < (3,):
    print("Python 2 has reached end-of-life and is not supported by SmartDashboard")
    sys.exit(-1)


from setuptools import setup
from setuptools.dist import Distribution


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
    version="0.0.1",
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

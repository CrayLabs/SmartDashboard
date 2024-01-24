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

import typing as t

import pytest

from smartdashboard.utils.ManifestReader import ManifestFileReader
from smartdashboard.utils.status import GREEN_RUNNING, StatusEnum
from smartdashboard.utils.StatusReader import get_experiment_status_summary


@pytest.mark.parametrize(
    "json_file, expected_status",
    [
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            f"Status: {GREEN_RUNNING}",
        ),
        pytest.param(
            "tests/utils/manifest_files/no_running.json",
            f"Status: {StatusEnum.INACTIVE.value}",
        ),
    ],
)
def test_get_experiment_status_summary(json_file, expected_status):
    manifest_file_reader = ManifestFileReader(json_file)
    manifest = manifest_file_reader.get_manifest()
    status = get_experiment_status_summary(manifest.runs)
    assert status == expected_status

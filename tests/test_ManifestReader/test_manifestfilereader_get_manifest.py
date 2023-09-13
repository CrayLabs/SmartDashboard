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

import pytest

from smartdashboard.utils.errors import MalformedManifestError, SSDashboardError
from smartdashboard.utils.ManifestReader import Manifest, ManifestFileReader


@pytest.mark.parametrize(
    "json_file, runs_length, app_length, orc_length, ens_length, return_type",
    [
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json", 2, 4, 3, 3, Manifest
        ),
        pytest.param(
            "tests/utils/manifest_files/no_experiment_manifest.json",
            0,
            0,
            0,
            0,
            Manifest,
        ),
        pytest.param(
            "tests/utils/manifest_files/no_apps_manifest.json",
            2,
            0,
            3,
            3,
            Manifest,
        ),
        pytest.param(
            "tests/utils/manifest_files/no_orchestrator_manifest.json",
            2,
            4,
            0,
            3,
            Manifest,
        ),
        pytest.param(
            "tests/utils/manifest_files/no_ensembles_manifest.json",
            2,
            4,
            3,
            0,
            Manifest,
        ),
        pytest.param(
            "tests/utils/manifest_files/malformed_apps.json",
            0,
            0,
            0,
            0,
            MalformedManifestError,
        ),
        pytest.param(
            "tests/utils/manifest_files/malformed_orcs.json",
            0,
            0,
            0,
            0,
            MalformedManifestError,
        ),
        pytest.param(
            "tests/utils/manifest_files/malformed_ensembles.json",
            0,
            0,
            0,
            0,
            MalformedManifestError,
        ),
    ],
)
def test_get_manifest(
    json_file, runs_length, app_length, orc_length, ens_length, return_type
):
    try:
        manifest_file_reader = ManifestFileReader(json_file)
        manifest = manifest_file_reader.get_manifest()
    except SSDashboardError as m:
        assert return_type == MalformedManifestError
        return
    assert len(manifest.runs) == runs_length
    assert len(manifest.applications) == app_length
    assert len(manifest.orchestrators) == orc_length
    assert len(manifest.ensembles) == ens_length
    assert type(manifest) == return_type

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

import pytest

from smartdashboard.utils.errors import *
from smartdashboard.utils.ManifestReader import ManifestFileReader
from smartdashboard.view_builders import *
from smartdashboard.views import *
from tests.utils.test_entities import *


@pytest.mark.parametrize(
    "function, json_file, return_type",
    [
        pytest.param(
            app_builder, "tests/utils/manifest_files/manifesttest.json", ApplicationView
        ),
        pytest.param(
            app_builder,
            "tests/utils/manifest_files/no_apps_manifest.json",
            ApplicationView,
        ),
        pytest.param(
            db_telem_builder,
            "tests/utils/manifest_files/manifesttest.json",
            DatabaseTelemetryView,
        ),
        pytest.param(
            db_telem_builder,
            "tests/utils/manifest_files/no_orchestrator_manifest.json",
            DatabaseTelemetryView,
        ),
        pytest.param(
            ens_builder, "tests/utils/manifest_files/manifesttest.json", EnsembleView
        ),
        pytest.param(
            ens_builder,
            "tests/utils/manifest_files/no_ensembles_manifest.json",
            EnsembleView,
        ),
        pytest.param(
            exp_builder, "tests/utils/manifest_files/manifesttest.json", ExperimentView
        ),
        pytest.param(
            orc_builder,
            "tests/utils/manifest_files/manifesttest.json",
            OrchestratorView,
        ),
        pytest.param(
            orc_builder,
            "tests/utils/manifest_files/no_orchestrator_manifest.json",
            OrchestratorView,
        ),
        pytest.param(
            overview_builder,
            "tests/utils/manifest_files/manifesttest.json",
            OverviewView,
        ),
    ],
)
def test_main_builders(function, json_file, return_type):
    manifest_file_reader = ManifestFileReader(json_file)
    manifest = manifest_file_reader.get_manifest()
    assert type(function(manifest)) == return_type


@pytest.mark.parametrize(
    "function, json_file, return_type",
    [
        pytest.param(
            client_view_builder,
            "tests/utils/manifest_files/manifesttest.json",
            ClientView,
        ),
        pytest.param(
            client_view_builder,
            "tests/utils/manifest_files/no_orchestrator_manifest.json",
            ClientView,
        ),
        pytest.param(
            memory_view_builder,
            "tests/utils/manifest_files/manifesttest.json",
            MemoryView,
        ),
        pytest.param(
            memory_view_builder,
            "tests/utils/manifest_files/no_orchestrator_manifest.json",
            MemoryView,
        ),
    ],
)
def test_db_content_builder(function, json_file, return_type):
    manifest_file_reader = ManifestFileReader(json_file)
    manifest = manifest_file_reader.get_manifest()
    orcs = manifest.orcs_with_run_ctx
    for orc in orcs:
        assert type(function(orc.entity.shards)) == return_type


@pytest.mark.parametrize(
    "orc",
    [
        pytest.param(orchestrator_1),
        pytest.param(orchestrator_2),
        pytest.param(orchestrator_3),
        pytest.param(orchestrator_4),
    ],
)
def test_orc_summary_builder(orc):
    assert type(orc_summary_builder(orc)) == OrchestratorSummaryView


@pytest.mark.parametrize(
    "error",
    [
        pytest.param(MalformedManifestError("Error message", "file", Exception())),
        pytest.param(ManifestError("Error message", "file", Exception())),
        pytest.param(SSDashboardError("Error message", "file", Exception())),
    ],
)
def test_error_builder(error):
    assert type(error_builder(error)) == ErrorView

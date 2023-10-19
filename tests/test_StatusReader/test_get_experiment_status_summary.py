import typing as t

import pytest

from smartdashboard.utils.ManifestReader import ManifestFileReader
from smartdashboard.utils.StatusReader import get_experiment_status_summary


@pytest.mark.parametrize(
    "json_file, expected_status",
    [
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json", "Status: :green[Running]"
        ),
        pytest.param(
            "tests/utils/manifest_files/no_running.json", "Status: :red[Inactive]"
        ),
        pytest.param(
            "tests/utils/manifest_files/no_experiment_manifest.json", "Status: "
        ),
    ],
)
def test_get_orchestrator_status_summary(json_file, expected_status):
    manifest_file_reader = ManifestFileReader(json_file)
    manifest = manifest_file_reader.get_manifest()
    status = get_experiment_status_summary(manifest.runs)
    assert status == expected_status

import pytest

from smartdashboard.utils.ManifestReader import ManifestFileReader


@pytest.mark.parametrize(
    "json_file, runs_length, app_length, orc_length, ens_length",
    [
        pytest.param("tests/test_utils/manifest_files/manifesttest.json", 2, 4, 3, 3),
        pytest.param(
            "tests/test_utils/manifest_files/no_experiment_manifest.json", 0, 0, 0, 0
        ),
        pytest.param(
            "tests/test_utils/manifest_files/no_apps_manifest.json", 2, 0, 3, 3
        ),
        pytest.param(
            "tests/test_utils/manifest_files/no_orchestrator_manifest.json", 2, 4, 0, 3
        ),
        pytest.param(
            "tests/test_utils/manifest_files/no_ensembles_manifest.json", 2, 4, 3, 0
        ),
    ],
)
def test_get_manifest(json_file, runs_length, app_length, orc_length, ens_length):
    manifest_file_reader = ManifestFileReader(json_file)
    manifest = manifest_file_reader.get_manifest()
    assert len(manifest.runs) == runs_length
    assert len(manifest.applications) == app_length
    assert len(manifest.orchestrators) == orc_length
    assert len(manifest.ensembles) == ens_length

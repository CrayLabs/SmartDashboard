import pytest

from smartdashboard.utils.errors import MalformedManifestError
from smartdashboard.utils.ManifestReader import Manifest, ManifestFileReader


@pytest.mark.parametrize(
    "json_file, runs_length, app_length, orc_length, ens_length, return_type",
    [
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json", 2, 4, 3, 3, Manifest
        ),
        pytest.param(
            "tests/test_utils/manifest_files/no_experiment_manifest.json",
            0,
            0,
            0,
            0,
            Manifest,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/no_apps_manifest.json",
            2,
            0,
            3,
            3,
            Manifest,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/no_orchestrator_manifest.json",
            2,
            4,
            0,
            3,
            Manifest,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/no_ensembles_manifest.json",
            2,
            4,
            3,
            0,
            Manifest,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/malformed_apps.json",
            0,
            0,
            0,
            0,
            MalformedManifestError,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/malformed_orcs.json",
            0,
            0,
            0,
            0,
            MalformedManifestError,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/malformed_ensembles.json",
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
    except MalformedManifestError as m:
        assert return_type == MalformedManifestError
        return
    assert len(manifest.runs) == runs_length
    assert len(manifest.applications) == app_length
    assert len(manifest.orchestrators) == orc_length
    assert len(manifest.ensembles) == ens_length
    assert type(manifest) == return_type

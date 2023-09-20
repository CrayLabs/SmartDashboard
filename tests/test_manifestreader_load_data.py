import pytest
from ..utils.FileReader import ManifestReader

parameterize_creator = pytest.mark.parametrize(
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
        pytest.param("file_doesnt_exist", 0, 0, 0, 0),
    ],
)


@parameterize_creator
def test_load_data(json_file, runs_length, app_length, orc_length, ens_length):
    dash_data = ManifestReader(json_file)
    assert len(dash_data.runs) == runs_length
    assert len(dash_data.applications) == app_length
    assert len(dash_data.orchestrators) == orc_length
    assert len(dash_data.ensembles) == ens_length

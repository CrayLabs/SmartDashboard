import pytest

from smartdashboard.utils.helpers import get_entities_with_name
from smartdashboard.utils.ManifestReader import ManifestFileReader
from tests.utils.test_entities import *


@pytest.mark.parametrize(
    "json_file, app_name, application",
    [
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "app1",
            application_1,
        ),
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "app2",
            application_2,
        ),
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "app3",
            application_3,
        ),
        pytest.param(
            "tests/utils/manifest_files/no_apps_manifest.json",
            "app1",
            None,
        ),
        pytest.param("file_doesnt_exist.json", "app4", FileNotFoundError),
    ],
)
def test_get_entity_apps(json_file, app_name, application):
    try:
        manifest_file_reader = ManifestFileReader(json_file)
        manifest = manifest_file_reader.get_manifest()
    except FileNotFoundError:
        assert FileNotFoundError == application
        return
    app = get_entities_with_name(app_name, manifest.applications)
    assert app == application


@pytest.mark.parametrize(
    "json_file, orc_name, orchestrator",
    [
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "orchestrator_1",
            orchestrator_1,
        ),
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "orchestrator_2",
            orchestrator_2,
        ),
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "orchestrator_3",
            orchestrator_3,
        ),
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "orc_doesnt_exist",
            None,
        ),
        pytest.param("file_doesnt_exist.json", "orchestrator_1", FileNotFoundError),
        pytest.param(
            "tests/utils/manifest_files/no_orchestrator_manifest.json",
            "orchestrator_1",
            None,
        ),
    ],
)
def test_get_entity_orchestrator(json_file, orc_name, orchestrator):
    try:
        manifest_file_reader = ManifestFileReader(json_file)
        manifest = manifest_file_reader.get_manifest()
    except FileNotFoundError:
        assert FileNotFoundError == orchestrator
        return
    orc = get_entities_with_name(orc_name, manifest.orchestrators)
    assert orc == orchestrator


@pytest.mark.parametrize(
    "json_file, ensemble_name, ensemble",
    [
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "ensemble_1",
            ensemble_1,
        ),
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "ensemble_3",
            ensemble_3,
        ),
        pytest.param("file_doesnt_exist.json", "ensemble4", FileNotFoundError),
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json",
            "ensemble_doesnt_exist",
            None,
        ),
        pytest.param(
            "tests/utils/manifest_files/no_ensembles_manifest.json",
            "ensemble_1",
            None,
        ),
    ],
)
def test_get_entity_ensemble(json_file, ensemble_name, ensemble):
    try:
        manifest_file_reader = ManifestFileReader(json_file)
        manifest = manifest_file_reader.get_manifest()
    except FileNotFoundError:
        assert FileNotFoundError == ensemble
        return
    ens = get_entities_with_name(ensemble_name, manifest.ensembles)
    assert ens == ensemble

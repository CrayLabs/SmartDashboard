import pytest
from ..utils.FileReader import ManifestReader
import tests.test_utils.test_entities as e


parameterize_creator = pytest.mark.parametrize(
    "json_file, app_name, application",
    [
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "app1",
            e.application_1,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "app2",
            e.application_2,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "app3",
            e.application_3,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/no_apps_manifest.json",
            "app1",
            None,
        ),
        pytest.param("file_doesnt_exist.json", "app4", None),
    ],
)


@parameterize_creator
def test_get_entity_apps(json_file, app_name, application):
    dash_data = ManifestReader(json_file)
    app = dash_data.get_entity(app_name, dash_data.applications)
    assert app == application


parameterize_creator = pytest.mark.parametrize(
    "json_file, orc_name, orchestrator",
    [
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "orchestrator_1",
            e.orchestrator_1,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "orchestrator_2",
            e.orchestrator_2,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "orchestrator_3",
            e.orchestrator_3,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "orc_doesnt_exist",
            None,
        ),
        pytest.param("file_doesnt_exist.json", "orchestrator_1", None),
        pytest.param(
            "tests/test_utils/manifest_files/no_orchestrator_manifest.json",
            "orchestrator_1",
            None,
        ),
    ],
)


@parameterize_creator
def test_get_entity_orchestrator(json_file, orc_name, orchestrator):
    dash_data = ManifestReader(json_file)
    orc = dash_data.get_entity(orc_name, dash_data.orchestrators)
    assert orc == orchestrator


parameterize_creator = pytest.mark.parametrize(
    "json_file, ensemble_name, ensemble",
    [
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "ensemble_1",
            e.ensemble_1,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "ensemble_3",
            e.ensemble_3,
        ),
        pytest.param("file_doesnt_exist.json", "ensemble4", None),
        pytest.param(
            "tests/test_utils/manifest_files/manifesttest.json",
            "ensemble_doesnt_exist",
            None,
        ),
        pytest.param(
            "tests/test_utils/manifest_files/no_ensembles_manifest.json",
            "ensemble_1",
            None,
        ),
    ],
)


@parameterize_creator
def test_get_entity_ensemble(json_file, ensemble_name, ensemble):
    dash_data = ManifestReader(json_file)
    ens = dash_data.get_entity(ensemble_name, dash_data.ensembles)
    assert ens == ensemble

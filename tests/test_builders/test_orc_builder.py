import pytest

from smartdashboard.utils.ManifestReader import ManifestFileReader
from smartdashboard.view_builders import orc_builder
from smartdashboard.views import OrchestratorView


@pytest.mark.parametrize(
    "json_file, return_type",
    [
        pytest.param("tests/utils/manifest_files/manifesttest.json", OrchestratorView),
    ],
)
def test_orc_builder(json_file, return_type):
    manifest_file_reader = ManifestFileReader(json_file)
    manifest = manifest_file_reader.get_manifest()
    assert type(orc_builder(manifest)) == return_type

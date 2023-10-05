import pytest

from smartdashboard.utils.ManifestReader import ManifestFileReader
from smartdashboard.view_builders import ens_builder
from smartdashboard.views import EnsembleView


@pytest.mark.parametrize(
    "json_file, return_type",
    [
        pytest.param("tests/test_utils/manifest_files/manifesttest.json", EnsembleView),
    ],
)
def test_ens_builder(json_file, return_type):
    manifest_file_reader = ManifestFileReader(json_file)
    manifest = manifest_file_reader.get_manifest()
    assert type(ens_builder(manifest)) == return_type

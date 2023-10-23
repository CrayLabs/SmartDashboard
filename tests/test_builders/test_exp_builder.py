import pytest

from smartdashboard.utils.ManifestReader import ManifestFileReader
from smartdashboard.view_builders import exp_builder


@pytest.mark.parametrize(
    "json_file, return_type",
    [
        pytest.param("tests/utils/manifest_files/manifesttest.json", type(None)),
    ],
)
def test_exp_builder(json_file, return_type):
    manifest_file_reader = ManifestFileReader(json_file)
    manifest = manifest_file_reader.get_manifest()
    assert type(exp_builder(manifest)) == return_type

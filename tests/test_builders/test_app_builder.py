import pytest

from smartdashboard.utils.ManifestReader import ManifestFileReader
from smartdashboard.view_builders import app_builder
from smartdashboard.views import ApplicationView


@pytest.mark.parametrize(
    "json_file, return_type",
    [
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json", ApplicationView
        ),
    ],
)
def test_app_builder(json_file, return_type):
    manifest_file_reader = ManifestFileReader(json_file)
    manifest = manifest_file_reader.get_manifest()
    assert type(app_builder(manifest)) == return_type

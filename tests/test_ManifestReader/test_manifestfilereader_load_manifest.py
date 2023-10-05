import pytest

from smartdashboard.utils.errors import ManifestError
from smartdashboard.utils.ManifestReader import Manifest, load_manifest


@pytest.mark.parametrize(
    "json_file, result_type",
    [
        pytest.param("tests/test_utils/manifest_files/manifesttest.json", Manifest),
        pytest.param("tests/test_utils/manifest_files/no_apps_manifest.json", Manifest),
        pytest.param("file_doesn't_exist.json", ManifestError),
        pytest.param(
            "tests/test_utils/manifest_files/JSONDecodererror.json", ManifestError
        ),
    ],
)
def test_load_manifest(json_file, result_type):
    try:
        manifest = load_manifest(json_file)
    except ManifestError as m:
        assert result_type == ManifestError
        return

    assert type(manifest) == result_type

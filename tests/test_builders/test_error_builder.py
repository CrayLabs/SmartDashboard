import pytest

from smartdashboard.utils.errors import (
    MalformedManifestError,
    ManifestError,
    SSDashboardError,
)
from smartdashboard.view_builders import error_builder
from smartdashboard.views import ErrorView


@pytest.mark.parametrize(
    "error, return_type",
    [
        pytest.param(
            MalformedManifestError("Error message", "file", Exception()), ErrorView
        ),
        pytest.param(ManifestError("Error message", "file", Exception()), ErrorView),
        pytest.param(SSDashboardError("Error message", "file", Exception()), ErrorView),
    ],
)
def test_error_builder(error, return_type):
    assert type(error_builder(error)) == return_type

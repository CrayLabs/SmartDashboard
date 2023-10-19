import typing as t

import pytest

from smartdashboard.utils.errors import MalformedManifestError
from smartdashboard.utils.StatusReader import get_status

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "entity, expected_status",
    [
        pytest.param(application_1, ("Completed", 0)),
        pytest.param(application_2, ("Failed", 1)),
        pytest.param(application_3, ("Running", None)),
        pytest.param(application_4, ("Completed", 0)),
        pytest.param(orch_1_shard_1, ("Running", None)),
        pytest.param(orch_1_shard_2, ("Failed", 1)),
        pytest.param(pending_shard, ("Pending", None)),
    ],
)
def test_get_status(entity: t.Dict[str, t.Any], expected_status):
    try:
        status_dir = entity["telemetry_metadata"]["status_dir"]
        status = get_status(status_dir)
    except MalformedManifestError:
        assert expected_status == MalformedManifestError
        return
    assert status == expected_status

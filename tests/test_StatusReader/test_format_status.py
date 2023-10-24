import typing as t

import pytest

from smartdashboard.utils.StatusReader import format_status, get_status

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "entity, expected_status",
    [
        pytest.param(application_1, "Status: :green[Completed]"),
        pytest.param(application_2, "Status: :red[Failed] with exit code 1"),
        pytest.param(application_3, "Status: :green[Running]"),
        pytest.param(application_4, "Status: :green[Completed]"),
        pytest.param(orch_1_shard_1, "Status: :green[Running]"),
        pytest.param(orch_1_shard_2, "Status: :red[Failed] with exit code 1"),
        pytest.param(pending_shard, "Status: Pending"),
    ],
)
def test_get_status(entity: t.Dict[str, t.Any], expected_status):
    status_dir = entity["telemetry_metadata"]["status_dir"]
    status = format_status(get_status(status_dir))
    assert status == expected_status

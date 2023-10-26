import typing as t

import pytest

from smartdashboard.utils.status import (
    GREEN_COMPLETED,
    GREEN_RUNNING,
    RED_FAILED,
    StatusEnum,
)
from smartdashboard.utils.StatusReader import format_status, get_status

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "entity, expected_status",
    [
        pytest.param(application_1, f"Status: {GREEN_COMPLETED}"),
        pytest.param(application_2, f"Status: {RED_FAILED}"),
        pytest.param(application_3, f"Status: {GREEN_RUNNING}"),
        pytest.param(application_4, f"Status: {GREEN_COMPLETED}"),
        pytest.param(orch_1_shard_1, f"Status: {GREEN_RUNNING}"),
        pytest.param(orch_1_shard_2, f"Status: {RED_FAILED}"),
        pytest.param(pending_shard, f"Status: {StatusEnum.PENDING.value}"),
    ],
)
def test_get_status(entity: t.Dict[str, t.Any], expected_status):
    status_dir = entity["telemetry_metadata"]["status_dir"]
    status = format_status(get_status(status_dir))
    assert status == expected_status

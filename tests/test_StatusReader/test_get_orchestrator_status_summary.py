import typing as t

import pytest

from smartdashboard.utils.status import StatusColors, StatusEnum
from smartdashboard.utils.StatusReader import get_orchestrator_status_summary

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "orchestrator, expected_status",
    [
        pytest.param(
            orchestrator_1, f"Status: {StatusColors.RED_UNSTABLE} (1 shard(s) failed)"
        ),
        pytest.param(
            orchestrator_2, f"Status: {StatusColors.RED_UNSTABLE} (1 shard(s) failed)"
        ),
        pytest.param(orchestrator_3, f"Status: {StatusColors.GREEN_RUNNING}"),
        pytest.param(
            orchestrator_4, f"Status: {StatusEnum.INACTIVE} (all shards completed)"
        ),
        pytest.param(no_shards_started, f"Status: {StatusEnum.PENDING}"),
        pytest.param(None, "Status: "),
    ],
)
def test_get_orchestrator_status_summary(
    orchestrator: t.Dict[str, t.Any], expected_status
):
    status = get_orchestrator_status_summary(orchestrator)
    assert status == expected_status

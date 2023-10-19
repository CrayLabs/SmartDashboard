import typing as t

import pytest

from smartdashboard.utils.StatusReader import get_orchestrator_status_summary

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "orchestrator, expected_status",
    [
        pytest.param(orchestrator_1, "Status: :red[Unstable (1 shard(s) failed)]"),
        pytest.param(orchestrator_2, "Status: :red[Unstable (1 shard(s) failed)]"),
        pytest.param(orchestrator_3, "Status: :green[Running]"),
        pytest.param(orchestrator_4, "Status: Inactive (all shards completed)"),
        pytest.param(no_shards_started, "Status: Pending"),
        pytest.param(None, "Status: "),
    ],
)
def test_get_orchestrator_status_summary(
    orchestrator: t.Dict[str, t.Any], expected_status
):
    status = get_orchestrator_status_summary(orchestrator)
    assert status == expected_status

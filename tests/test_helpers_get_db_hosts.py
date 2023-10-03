import pytest

from smartdashboard.utils.helpers import get_db_hosts

from tests.test_utils.test_entities import *


@pytest.mark.parametrize(
    "orchestrator, expected_value",
    [
        pytest.param(orchestrator_1, ["shard1_host", "shard2_host"]),
        pytest.param(orchestrator_2, ["shard1_host", "shard2_host"]),
        pytest.param(orchestrator_3, ["shard1_host"]),
        pytest.param(application_1, []),
        pytest.param(no_shards_orchestrator, []),
    ],
)
def test_get_db_hosts(orchestrator, expected_value):
    hosts = get_db_hosts(orchestrator)
    assert hosts == expected_value

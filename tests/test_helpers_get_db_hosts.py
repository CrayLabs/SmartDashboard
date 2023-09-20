import pytest
import tests.test_utils.test_entities as e
from utils.helpers import get_db_hosts


parameterize_creator = pytest.mark.parametrize(
    "orchestrator, expected_value",
    [
        pytest.param(e.orchestrator_1, ["shard1_host", "shard2_host"]),
        pytest.param(e.orchestrator_2, ["shard1_host", "shard2_host"]),
        pytest.param(e.orchestrator_3, ["shard1_host"]),
        pytest.param(e.application_1, []),
        pytest.param(e.no_shards_orchestrator, []),
    ],
)


@parameterize_creator
def test_get_db_hosts(orchestrator, expected_value):
    hosts = get_db_hosts(orchestrator)
    assert hosts == expected_value

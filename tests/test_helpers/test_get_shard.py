import pytest

from smartdashboard.utils.helpers import get_shard

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "shard_name, orc, shard",
    [
        pytest.param("shard 1", orchestrator_1, orch_1_shard_1),
        pytest.param("shard 2", orchestrator_1, orch_1_shard_2),
        pytest.param("shard doesnt_exist", orchestrator_1, None),
        pytest.param("shard 1", None, None),
    ],
)
def test_get_shard(shard_name, orc, shard):
    sh = get_shard(shard_name, orc)
    assert sh == shard

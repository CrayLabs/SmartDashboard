import pytest

from smartdashboard.utils.helpers import get_shard

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "shard_name, orc, shard",
    [
        pytest.param("shard 1", orchestrator_1, orch_1_shard_1),
        # pytest.param("ensemble_3_member_1", ensemble_3, ensemble_3_member_1),
        # pytest.param("ensemble_3_member_2", ensemble_3, ensemble_3_member_2),
        # pytest.param("ensemble_2_member_ doesnt_exist", ensemble_2, None),
        # pytest.param("ensemble_2_member_ doesnt_exist", None, None),
    ],
)
def test_get_shard(shard_name, orc, shard):
    sh = get_shard(shard_name, orc)
    assert sh == shard

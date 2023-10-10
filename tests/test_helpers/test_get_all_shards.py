import pytest

from smartdashboard.utils.helpers import get_all_shards

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "orc, expected_length, expected_value",
    [
        pytest.param(orchestrator_1, 2, orchestrator_1.get("shards")),
        pytest.param(orchestrator_2, 2, orchestrator_2.get("shards")),
        pytest.param(orchestrator_3, 1, orchestrator_3.get("shards")),
        pytest.param(None, 0, []),
    ],
)
def test_get_all_shards(orc, expected_length, expected_value):
    val = get_all_shards(orc)
    assert len(val) == expected_length
    assert val == expected_value

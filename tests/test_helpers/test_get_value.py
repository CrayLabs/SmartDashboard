import pytest

from smartdashboard.utils.helpers import get_value
from ..utils.test_entities import *


@pytest.mark.parametrize(
    "key, entity, expected_value",
    [
        pytest.param("name", application_1, "app1"),
        pytest.param("path", application_1, "app/1/path"),
        pytest.param("type", orchestrator_1, "redis"),
        pytest.param("perm_strat", ensemble_2, "all-perm"),
        pytest.param("path", ensemble_3_member_1, "member 1 path"),
        pytest.param("path", None, ""),
        pytest.param("key doesn't exist", application_1, ""),
    ],
)
def test_get_value(key, entity, expected_value):
    val = get_value(key, entity)
    assert val == expected_value

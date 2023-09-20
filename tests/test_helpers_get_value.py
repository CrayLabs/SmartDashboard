import pytest
import tests.test_utils.test_entities as e
from utils.helpers import get_value


parameterize_creator = pytest.mark.parametrize(
    "key, entity, expected_value",
    [
        pytest.param("name", e.application_1, "app1"),
        pytest.param("path", e.application_1, "app/1/path"),
        pytest.param("type", e.orchestrator_1, "redis"),
        pytest.param("perm_strat", e.ensemble_2, "all-perm"),
        pytest.param("path", e.ensemble_3_member_1, "member 1 path"),
        pytest.param("path", None, ""),
        pytest.param("key doesn't exist", e.application_1, ""),
    ],
)


@parameterize_creator
def test_get_value(key, entity, expected_value):
    val = get_value(key, entity)
    assert val == expected_value

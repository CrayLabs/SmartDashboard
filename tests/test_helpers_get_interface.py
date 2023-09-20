import pytest
import tests.test_utils.test_entities as e
from utils.helpers import get_interface


parameterize_creator = pytest.mark.parametrize(
    "entity, expected_value",
    [
        pytest.param(e.orchestrator_1, "lo, lo2"),
        pytest.param(e.orchestrator_2, "lo"),
        pytest.param(e.orchestrator_3, "lo"),
        pytest.param(e.application_1, ""),
    ],
)


@parameterize_creator
def test_get_interface(entity, expected_value):
    val = get_interface(entity)
    assert val == expected_value

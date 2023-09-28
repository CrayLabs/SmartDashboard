import pytest
from .test_utils.test_entities import *
from utils.helpers import get_interface


@pytest.mark.parametrize(
    "entity, expected_value",
    [
        pytest.param(orchestrator_1, "lo, lo2"),
        pytest.param(orchestrator_2, "lo"),
        pytest.param(orchestrator_3, "lo"),
        pytest.param(application_1, ""),
    ],
)
def test_get_interface(entity, expected_value):
    val = get_interface(entity)
    assert val == expected_value

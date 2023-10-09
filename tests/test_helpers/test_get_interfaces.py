import pytest

from smartdashboard.utils.helpers import get_interfaces
from ..utils.test_entities import *


@pytest.mark.parametrize(
    "entity, expected_value",
    [
        pytest.param(orchestrator_1, "lo, lo2"),
        pytest.param(orchestrator_2, "lo"),
        pytest.param(orchestrator_3, "lo"),
        pytest.param(application_1, ""),
    ],
)
def test_get_interfaces(entity, expected_value):
    val = get_interfaces(entity)
    assert val == expected_value

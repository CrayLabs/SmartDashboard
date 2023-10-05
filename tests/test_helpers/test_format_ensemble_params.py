import pytest

from smartdashboard.utils.helpers import format_ensemble_params
from tests.test_utils.test_entities import *


@pytest.mark.parametrize(
    "entity, expected_key_value_list",
    [
        pytest.param(ensemble_1, [("string", "Any1, Any3")]),
        pytest.param(ensemble_2, [("string", "Any1, Any2, Any3")]),
        pytest.param(ensemble_3, [("string", "Any1, Any2, Any3")]),
        pytest.param(None, []),
        pytest.param(orchestrator_1, []),
    ],
)
def test_format_ensemble_params(entity, expected_key_value_list):
    key_and_values = format_ensemble_params(entity)
    assert key_and_values == expected_key_value_list

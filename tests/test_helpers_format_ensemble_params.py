import pytest
from .test_utils.test_entities import *
from utils.helpers import format_ensemble_params


@pytest.mark.parametrize(
    "entity, expected_keys, expected_values",
    [
        pytest.param(ensemble_1, ["string"], ["Any1, Any3"]),
        pytest.param(ensemble_2, ["string"], ["Any1, Any2, Any3"]),
        pytest.param(ensemble_3, ["string"], ["Any1, Any2, Any3"]),
        pytest.param(None, [], []),
        pytest.param(orchestrator_1, [], []),
    ],
)
def test_format_ensemble_params(entity, expected_keys, expected_values):
    k, v = format_ensemble_params(entity)
    assert k == expected_keys
    assert v == expected_values

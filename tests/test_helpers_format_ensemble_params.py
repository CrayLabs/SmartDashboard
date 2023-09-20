import pytest
import tests.test_utils.test_entities as e
from utils.helpers import format_ensemble_params


parameterize_creator = pytest.mark.parametrize(
    "ensemble, expected_keys, expected_values",
    [
        pytest.param(e.ensemble_1, ["string"], ["Any1, Any3"]),
        pytest.param(e.ensemble_2, ["string"], ["Any1, Any2, Any3"]),
        pytest.param(e.ensemble_3, ["string"], ["Any1, Any2, Any3"]),
        pytest.param(None, [], []),
        pytest.param(e.orchestrator_1, [], []),
    ],
)


@parameterize_creator
def test_format_ensemble_params(ensemble, expected_keys, expected_values):
    k, v = format_ensemble_params(ensemble)
    assert k == expected_keys
    assert v == expected_values

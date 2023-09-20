import pytest
import tests.test_utils.test_entities as e
from utils.helpers import get_ensemble_members


parameterize_creator = pytest.mark.parametrize(
    "ensemble, expected_length, expected_value",
    [
        pytest.param(e.ensemble_1, 1, e.ensemble_1.get("models")),
        pytest.param(e.ensemble_2, 0, e.ensemble_2.get("models")),
        pytest.param(None, 0, []),
    ],
)


@parameterize_creator
def test_get_ensemble_members(ensemble, expected_length, expected_value):
    val = get_ensemble_members(ensemble)
    assert len(val) == expected_length
    assert val == expected_value

import pytest
from .test_utils.test_entities import *
from utils.helpers import get_ensemble_members


@pytest.mark.parametrize(
    "ensemble, expected_length, expected_value",
    [
        pytest.param(ensemble_1, 1, ensemble_1.get("models")),
        pytest.param(ensemble_2, 0, ensemble_2.get("models")),
        pytest.param(None, 0, []),
    ],
)
def test_get_ensemble_members(ensemble, expected_length, expected_value):
    val = get_ensemble_members(ensemble)
    assert len(val) == expected_length
    assert val == expected_value

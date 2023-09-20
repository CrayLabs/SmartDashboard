import pytest
import tests.test_utils.test_entities as e
from utils.helpers import get_exe_args


parameterize_creator = pytest.mark.parametrize(
    "entity, expected_value",
    [
        pytest.param(e.application_1, ["string"]),
        pytest.param(e.application_2, ["string1", "string2", "string3"]),
        pytest.param(None, []),
    ],
)


@parameterize_creator
def test_get_exe_args(entity, expected_value):
    val = get_exe_args(entity)
    assert val == expected_value

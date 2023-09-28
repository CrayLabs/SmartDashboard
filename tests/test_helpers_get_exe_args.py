import pytest
from .test_utils.test_entities import *
from utils.helpers import get_exe_args


@pytest.mark.parametrize(
    "entity, expected_value",
    [
        pytest.param(application_1, ["string"]),
        pytest.param(application_2, ["string1", "string2", "string3"]),
        pytest.param(None, []),
    ],
)
def test_get_exe_args(entity, expected_value):
    val = get_exe_args(entity)
    assert val == expected_value

import pytest

from smartdashboard.utils.helpers import get_exe_args
from tests.test_utils.test_entities import *


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

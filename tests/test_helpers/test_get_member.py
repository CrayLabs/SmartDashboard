import pytest

from smartdashboard.utils.helpers import get_member

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "member_name, ensemble, member",
    [
        pytest.param("ensemble_1_member_1", ensemble_1, ensemble_1_member_1),
        pytest.param("ensemble_3_member_1", ensemble_3, ensemble_3_member_1),
        pytest.param("ensemble_3_member_2", ensemble_3, ensemble_3_member_2),
        pytest.param("ensemble_2_member_ doesnt_exist", ensemble_2, None),
        pytest.param("ensemble_2_member_ doesnt_exist", None, None),
    ],
)
def test_get_member(member_name, ensemble, member):
    mem = get_member(member_name, ensemble)
    assert mem == member

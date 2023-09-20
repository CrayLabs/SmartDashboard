import pytest
import tests.test_utils.test_entities as e
from utils.helpers import get_member


parameterize_creator = pytest.mark.parametrize(
    "member_name, ensemble, member",
    [
        pytest.param("ensemble_1_member_1", e.ensemble_1, e.ensemble_1_member_1),
        pytest.param("ensemble_3_member_1", e.ensemble_3, e.ensemble_3_member_1),
        pytest.param("ensemble_3_member_2", e.ensemble_3, e.ensemble_3_member_2),
        pytest.param("ensemble_2_member_ doesnt_exist", e.ensemble_2, None),
        pytest.param("ensemble_2_member_ doesnt_exist", None, None),
    ],
)


@parameterize_creator
def test_get_member(member_name, ensemble, member):
    mem = get_member(member_name, ensemble)
    assert mem == member

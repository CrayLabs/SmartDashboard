import pytest

from smartdashboard.utils.helpers import get_port
from tests.test_utils.test_entities import *


@pytest.mark.parametrize(
    "orchestrator, expected_port",
    [
        pytest.param(orchestrator_1, "11111"),
        pytest.param(orchestrator_2, "22222"),
        pytest.param(orchestrator_3, "12345"),
        pytest.param(mismatched_port_orchestrator, Exception),
        pytest.param(None, ""),
    ],
)
def test_get_port(orchestrator, expected_port):
    if expected_port == Exception:
        with pytest.raises(Exception) as excinfo:
            port = get_port(orchestrator)
        assert (
            str(excinfo.value)
            == "Shards within an Orchestrator should have the same port."
        )
    else:
        port = get_port(orchestrator)
        assert port == expected_port

import pytest

from smartdashboard.utils.helpers import get_port

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "orchestrator, expected_port",
    [
        pytest.param(orchestrator_1, "11111"),
        pytest.param(orchestrator_2, "22222"),
        pytest.param(orchestrator_3, "12345"),
        pytest.param(
            mismatched_port_orchestrator,
            "Warning! Shards within an Orchestrator should have the same port. 11111, 11211",
        ),
        pytest.param(None, ""),
    ],
)
def test_get_port(orchestrator, expected_port):
    port = get_port(orchestrator)
    assert port == expected_port

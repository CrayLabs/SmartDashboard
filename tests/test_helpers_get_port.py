import pytest
import tests.test_utils.test_entities as e
from utils.helpers import get_port


parameterize_creator = pytest.mark.parametrize(
    "orchestrator, expected_port",
    [
        pytest.param(e.orchestrator_1, "11111"),
        pytest.param(e.orchestrator_2, "22222"),
        pytest.param(e.orchestrator_3, "12345"),
        pytest.param(e.mismatched_port_orchestrator, Exception),
        pytest.param(None, ""),
    ],
)


@parameterize_creator
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

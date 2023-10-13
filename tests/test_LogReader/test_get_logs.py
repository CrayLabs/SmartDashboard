import pytest

import tests.utils.test_entities as e
from smartdashboard.utils.helpers import get_value
from smartdashboard.utils.LogReader import get_logs

parameterize_creator = pytest.mark.parametrize(
    "entity, expected_output_log, expected_error_log",
    [
        pytest.param(
            e.application_1,
            e.model0_out_logs,
            e.model0_err_logs,
        ),
        pytest.param(
            e.application_2,
            e.model1_out_logs,
            e.model1_err_logs,
        ),
        pytest.param(
            None,
            "",
            "",
        ),
    ],
)


@parameterize_creator
def test_load_log_data(entity, expected_output_log, expected_error_log):
    output_log_path = get_value("out_file", entity)
    error_log_path = get_value("err_file", entity)
    output_logs = get_logs(output_log_path)
    error_logs = get_logs(error_log_path)
    assert output_logs == expected_output_log
    assert error_logs == expected_error_log

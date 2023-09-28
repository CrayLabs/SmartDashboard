import pytest
from .test_utils.test_entities import *
from utils.helpers import format_mixed_nested_dict


@pytest.mark.parametrize(
    "dict_name, entity, expected_keys, expected_values",
    [
        pytest.param(
            "batch_settings",
            application_1,
            ["batch_cmd", "arg1", "arg2"],
            ["command", "string1", "None"],
        ),
        pytest.param(
            "run_settings",
            application_1,
            ["exe", "run_command", "arg1", "arg2"],
            ["echo", "srun", "string1", "None"],
        ),
        pytest.param("params", ensemble_1_member_1, ["string"], ["Any"]),
        pytest.param(
            "files",
            application_2,
            ["Symlink", "Symlink", "Configure", "Copy", "Copy"],
            ["file1", "file2", "file3", "file4", "file5"],
        ),
        pytest.param(
            "settings",
            ensemble_1_member_1.get("colocated_db"),
            ["protocol", "port", "interface", "db_cpus", "limit_app_cpus", "debug"],
            ["TCP/IP", "1111", "lo", "1", "True", "False"],
        ),
        pytest.param("doesnt_exist", ensemble_1_member_1, [], []),
        pytest.param("batch_settings", None, [], []),
    ],
)
def test_format_mixed_nested_dict(dict_name, entity, expected_keys, expected_values):
    k, v = format_mixed_nested_dict(dict_name, entity)
    assert k == expected_keys
    assert v == expected_values

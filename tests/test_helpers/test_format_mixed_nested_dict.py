import pytest

from smartdashboard.utils.helpers import flatten_nested_keyvalue_containers

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "dict_name, entity, expected_list",
    [
        pytest.param(
            "batch_settings",
            application_1,
            [("batch_cmd", "command"), ("arg1", "string1"), ("arg2", "None")],
        ),
        pytest.param(
            "run_settings",
            application_1,
            [
                ("exe", "echo"),
                ("run_command", "srun"),
                ("arg1", "string1"),
                ("arg2", "None"),
            ],
        ),
        pytest.param("params", ensemble_1_member_1, [("string", "Any")]),
        pytest.param(
            "files",
            application_2,
            [
                ("Symlink", "file1"),
                ("Symlink", "file2"),
                ("Configure", "file3"),
                ("Copy", "file4"),
                ("Copy", "file5"),
            ],
        ),
        pytest.param(
            "settings",
            ensemble_1_member_1.get("colocated_db"),
            [
                ("protocol", "TCP/IP"),
                ("port", "1111"),
                ("interface", "lo"),
                ("db_cpus", "1"),
                ("limit_app_cpus", "True"),
                ("debug", "False"),
            ],
        ),
        pytest.param("doesnt_exist", ensemble_1_member_1, []),
        pytest.param("batch_settings", None, []),
    ],
)
def test_flatten_nested_keyvalue_containers(dict_name, entity, expected_list):
    key_value_list = flatten_nested_keyvalue_containers(dict_name, entity)
    assert key_value_list == expected_list

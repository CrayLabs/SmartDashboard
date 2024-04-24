# BSD 2-Clause License
#
# Copyright (c) 2021-2024, Hewlett Packard Enterprise
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import pytest

from smartdashboard.utils.helpers import flatten_nested_keyvalue_containers

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "dict_name, entity, expected_list",
    [
        pytest.param(
            "batch_settings",
            application_1.dict(),
            [("batch_cmd", "command"), ("arg1", "string1"), ("arg2", "None")],
        ),
        pytest.param(
            "run_settings",
            application_1.dict(),
            [
                ("exe", "echo"),
                ("run_command", "srun"),
                ("arg1", "string1"),
                ("arg2", "None"),
            ],
        ),
        pytest.param("params", ensemble_1.models[0].dict(), [("string", "Any")]),
        pytest.param(
            "files",
            application_2.dict(),
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
            ensemble_1.models[0].colocated_db,
            [
                ("protocol", "TCP/IP"),
                ("port", "1111"),
                ("interface", "lo"),
                ("db_cpus", "1"),
                ("limit_app_cpus", "True"),
                ("debug", "False"),
            ],
        ),
        pytest.param("doesnt_exist", ensemble_1.models[0].dict(), []),
        pytest.param("batch_settings", None, []),
    ],
)
def test_flatten_nested_keyvalue_containers(dict_name, entity, expected_list):
    key_value_list = flatten_nested_keyvalue_containers(dict_name, entity)
    assert key_value_list == expected_list

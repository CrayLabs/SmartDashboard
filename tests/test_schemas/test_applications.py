# BSD 2-Clause License
#
# Copyright (c) 2021-2023, Hewlett Packard Enterprise
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

from tests.utils.test_entities import *


@pytest.mark.parametrize(
    "entity, expected_value",
    [
        pytest.param(
            application_1,
            {
                "Name": ("model1", "model2", "script1", "script2"),
                "Type": ("DB Model", "DB Model", "DB Script", "DB Script"),
                "Backend": ("model1_tf", "model2_tf", "script1_torch", "script2_torch"),
                "Device": ("model1_cpu", "model2_cpu", "script1_cpu", "script2_gpu"),
            },
        ),
        pytest.param(
            application_2,
            {
                "Name": ("model1", "model2", "script1", "script2"),
                "Type": ("DB Model", "DB Model", "DB Script", "DB Script"),
                "Backend": ("model1_tf", "model2_tf", "script1_torch", "script2_torch"),
                "Device": ("model1_cpu", "model2_cpu", "script1_cpu", "script2_gpu"),
            },
        ),
        pytest.param(
            no_db_scripts_or_models,
            {"Backend": (), "Device": (), "Name": (), "Type": ()},
        ),
        pytest.param(
            application_3,
            {
                "Name": ("model1", "model2"),
                "Type": ("DB Model", "DB Model"),
                "Backend": ("model1_tf", "model2_tf"),
                "Device": ("model1_cpu", "model2_cpu"),
            },
        ),
        pytest.param(
            application_4,
            {
                "Name": ("script1", "script2"),
                "Type": ("DB Script", "DB Script"),
                "Backend": ("script1_torch", "script2_torch"),
                "Device": ("script1_cpu", "script2_gpu"),
            },
        ),
    ],
)
def test_get_loaded_entities(entity: Application, expected_value):
    val = entity.loaded_entities
    assert val == expected_value


@pytest.mark.parametrize(
    "entity, expected_value",
    [
        pytest.param(application_1, ["string"]),
        pytest.param(application_2, ["string1", "string2", "string3"]),
        pytest.param(ensemble_3.models[1], ["string"]),
    ],
)
def test_get_exe_args(entity: Application, expected_value):
    val = entity.exe_args
    assert val == expected_value

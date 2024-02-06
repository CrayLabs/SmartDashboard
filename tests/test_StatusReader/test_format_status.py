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

import typing as t

import pytest

from smartdashboard.utils.status import (
    GREEN_COMPLETED,
    GREEN_RUNNING,
    RED_FAILED,
    StatusEnum,
)
from smartdashboard.utils.StatusReader import format_status, get_status

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "entity, expected_status",
    [
        pytest.param(application_1, f"Status: {GREEN_COMPLETED}"),
        pytest.param(application_2, f"Status: {RED_FAILED}"),
        pytest.param(application_3, f"Status: {GREEN_RUNNING}"),
        pytest.param(application_4, f"Status: {GREEN_COMPLETED}"),
        pytest.param(orchestrator_1.shards[0], f"Status: {GREEN_RUNNING}"),
        pytest.param(orchestrator_1.shards[1], f"Status: {RED_FAILED}"),
        pytest.param(pending_shard, f"Status: {StatusEnum.UNKNOWN.value}"),
        pytest.param(
            malformed_status_dir_shard, f"Status: {StatusEnum.MALFORMED.value}"
        ),
    ],
)
def test_get_status(entity: t.Dict[str, t.Any], expected_status):
    try:
        status_dir = entity.telemetry_metadata["status_dir"]
        status = format_status(get_status(status_dir))
    except KeyError:
        assert expected_status == f"Status: {StatusEnum.MALFORMED.value}"
        return
    assert status == expected_status

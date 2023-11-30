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

from smartdashboard.utils.errors import MalformedManifestError
from smartdashboard.utils.status import StatusEnum
from smartdashboard.utils.StatusReader import StatusData, get_status

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "entity, expected_status",
    [
        pytest.param(application_1, StatusData(StatusEnum.COMPLETED, 0)),
        pytest.param(application_2, StatusData(StatusEnum.FAILED, 1)),
        pytest.param(application_3, StatusData(StatusEnum.RUNNING, None)),
        pytest.param(application_4, StatusData(StatusEnum.COMPLETED, 0)),
        pytest.param(orch_1_shard_1, StatusData(StatusEnum.RUNNING, None)),
        pytest.param(orch_1_shard_2, StatusData(StatusEnum.FAILED, 1)),
        pytest.param(pending_shard, StatusData(StatusEnum.PENDING, None)),
        pytest.param(malformed_status_dir_shard, StatusData(StatusEnum.UNKNOWN, None)),
        pytest.param(no_return_code_shard, StatusData(StatusEnum.UNKNOWN, None)),
        pytest.param(
            JSONDecoderError_status_shard, StatusData(StatusEnum.UNKNOWN, None)
        ),
    ],
)
def test_get_status(entity, expected_status):
    try:
        status_dir = entity.telemetry_metadata["status_dir"]
        status = get_status(status_dir)
    except MalformedManifestError:
        assert expected_status == MalformedManifestError
        return
    except KeyError:
        assert expected_status == StatusData(StatusEnum.UNKNOWN, None)
        return
    assert status == expected_status

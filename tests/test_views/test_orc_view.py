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

from smartdashboard.views import OrchestratorView
from tests.utils.test_entities import *


@pytest.mark.parametrize(
    "orc, shard, status_string, out_logs, err_logs",
    [
        pytest.param(
            orchestrator_1,
            orchestrator_1.shards[0],
            "Status: :red[Unstable] (1 shard(s) failed)",
            model1_out_logs,
            model1_err_logs,
        ),
        pytest.param(
            orchestrator_2,
            orchestrator_2.shards[1],
            "Status: :red[Unstable] (1 shard(s) failed)",
            model1_out_logs,
            model1_err_logs,
        ),
        pytest.param(
            no_shards_started,
            no_shards_started.shards[0],
            "Status: Unknown",
            model0_out_logs,
            model0_err_logs,
        ),
    ],
)
def test_orc_view(orc, shard, status_string, out_logs, err_logs):
    view = OrchestratorView(orc, shard)
    assert view.view_model == shard
    assert view.status == status_string
    assert view.out_logs == out_logs
    assert view.err_logs == err_logs

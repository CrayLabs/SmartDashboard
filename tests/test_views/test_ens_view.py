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

from smartdashboard.views import EnsembleView
from tests.utils.test_entities import *


@pytest.mark.parametrize(
    "ensemble, member, status_string, member_status_string, out_logs, err_logs",
    [
        pytest.param(
            ensemble_1,
            ensemble_1.models[0],
            "Status: 0 Running, 1 Completed, 0 Failed, 0 Unknown, 0 Malformed",
            "Status: :green[Completed]",
            model0_out_logs,
            model0_err_logs,
        ),
        pytest.param(
            ensemble_2,
            None,
            "Status: 0 Running, 0 Completed, 0 Failed, 0 Unknown, 0 Malformed",
            "Status: ",
            "",
            "",
        ),
        pytest.param(
            ensemble_4,
            ensemble_4.models[0],
            "Status: 0 Running, 0 Completed, 2 Failed, 0 Unknown, 0 Malformed",
            "Status: :red[Failed]",
            model0_out_logs,
            model0_err_logs,
        ),
    ],
)
def test_ensemble_view(
    ensemble, member, status_string, member_status_string, out_logs, err_logs
):
    view = EnsembleView(ensemble, member)
    assert view.view_model == member
    assert view.member_status == member_status_string
    assert view.status == status_string
    assert view.out_logs == out_logs
    assert view.err_logs == err_logs

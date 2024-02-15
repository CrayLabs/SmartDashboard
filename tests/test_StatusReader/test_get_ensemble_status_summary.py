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

from smartdashboard.utils.StatusReader import get_ensemble_status_summary

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "ensemble, expected_status",
    [
        pytest.param(
            ensemble_1,
            "Status: 0 Running, 1 Completed, 0 Failed, 0 Unknown, 0 Malformed",
        ),
        pytest.param(
            ensemble_2,
            "Status: 0 Running, 0 Completed, 0 Failed, 0 Unknown, 0 Malformed",
        ),
        pytest.param(
            ensemble_3,
            "Status: 1 Running, 0 Completed, 1 Failed, 0 Unknown, 0 Malformed",
        ),
        pytest.param(
            ensemble_4,
            "Status: 0 Running, 0 Completed, 2 Failed, 0 Unknown, 0 Malformed",
        ),
        pytest.param(
            ensemble_5,
            "Status: 0 Running, 0 Completed, 0 Failed, 2 Unknown, 0 Malformed",
        ),
        pytest.param(None, "Status: "),
    ],
)
def test_get_ensemble_status_summary(ensemble: t.Dict[str, t.Any], expected_status):
    status = get_ensemble_status_summary(ensemble)
    assert status == expected_status

import typing as t

import pytest

from smartdashboard.utils.StatusReader import get_ensemble_status_summary

from ..utils.test_entities import *


@pytest.mark.parametrize(
    "ensemble, expected_status",
    [
        pytest.param(
            ensemble_1, "Status: 0 Running, 1 Completed, 0 Failed, 0 Pending, 0 Unknown"
        ),
        pytest.param(
            ensemble_2, "Status: 0 Running, 0 Completed, 0 Failed, 0 Pending, 0 Unknown"
        ),
        pytest.param(
            ensemble_3, "Status: 1 Running, 0 Completed, 1 Failed, 0 Pending, 0 Unknown"
        ),
        pytest.param(
            ensemble_4, "Status: 0 Running, 0 Completed, 2 Failed, 0 Pending, 0 Unknown"
        ),
        pytest.param(None, "Status: "),
    ],
)
def test_get_ensemble_status_summary(ensemble: t.Dict[str, t.Any], expected_status):
    status = get_ensemble_status_summary(ensemble)
    assert status == expected_status

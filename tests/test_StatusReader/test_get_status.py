import typing as t

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
    ],
)
def test_get_status(entity: t.Dict[str, t.Any], expected_status):
    try:
        status_dir = entity["telemetry_metadata"]["status_dir"]
        status = get_status(status_dir)
    except MalformedManifestError:
        assert expected_status == MalformedManifestError
        return
    except KeyError:
        assert expected_status == StatusData(StatusEnum.UNKNOWN, None)
        return
    assert status == expected_status

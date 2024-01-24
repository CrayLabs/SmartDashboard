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

import itertools
import json
import os
import typing as t
from dataclasses import dataclass

from smartdashboard.schemas.application import Application
from smartdashboard.schemas.ensemble import Ensemble
from smartdashboard.schemas.orchestrator import Orchestrator
from smartdashboard.schemas.run import Run
from smartdashboard.schemas.shard import Shard

from .status import GREEN_COMPLETED, GREEN_RUNNING, RED_FAILED, RED_UNSTABLE, StatusEnum


@dataclass(frozen=True)
class StatusData:
    """Data class representing entity status

    :param status: Status enum of the entity
    :type status: StatusEnum
    :param return_code: Return code of the entity
    :type return_code: Optional[int]
    """

    status: StatusEnum
    return_code: t.Optional[int]


def get_status(dir_path: str) -> StatusData:
    """Get the status of an application or shard

    This function is used to get the status of
    applications and shards. Status summary
    functions also use this to get the status
    of each of their members.

    :param dir_path: Directory of the entity
    :type dir_path: str
    :return: Status enum and return code
    :rtype: StatusData
    """
    start_json_path = os.path.join(dir_path, "start.json")
    stop_json_path = os.path.join(dir_path, "stop.json")

    if os.path.exists(start_json_path):
        if os.path.exists(stop_json_path):
            try:
                with open(stop_json_path, "r", encoding="utf-8") as stop_json_file:
                    stop_data = json.load(stop_json_file)
            except json.JSONDecodeError:
                return StatusData(StatusEnum.UNKNOWN, None)

            try:
                status = (
                    StatusData(StatusEnum.FAILED, stop_data["return_code"])
                    if stop_data["return_code"] != 0
                    else StatusData(StatusEnum.COMPLETED, stop_data["return_code"])
                )

            except KeyError:
                status = StatusData(StatusEnum.UNKNOWN, None)

            return status

        return StatusData(StatusEnum.RUNNING, None)

    return StatusData(StatusEnum.PENDING, None)


def get_ensemble_status_summary(ensemble: t.Optional[Ensemble]) -> str:
    """Get the status summary of an ensemble

    Gets the status of each member and returns
    a summary of the overall ensemble.

    :param ensemble: Ensemble
    :type ensemble: Optional[Ensemble]
    :return: Status summary
    :rtype: str
    """
    status_str = "Status: "

    if ensemble:
        status_counts = status_mapping(ensemble.models)

        formatted_counts = [
            f"{count} {status.value}" for status, count in status_counts.items()
        ]

        status_description = f"{status_str}{', '.join(formatted_counts)}"

        return status_description

    return status_str


def get_orchestrator_status_summary(orchestrator: t.Optional[Orchestrator]) -> str:
    """Get the status summary of an orchestrator

    Gets the status of each shard and returns
    a summary of the overall orchestrator.

    :param orchestrator: Orchestrator
    :type orchestrator: Optional[Orchestrator]
    :return: Status summary
    :rtype: str
    """
    status_str = "Status: "

    if orchestrator:
        status_counts = status_mapping(orchestrator.shards)

        if status_counts[StatusEnum.COMPLETED] == sum(status_counts.values()):
            return f"{status_str}{StatusEnum.INACTIVE.value} (all shards completed)"

        if status_counts[StatusEnum.PENDING] == sum(status_counts.values()):
            return f"{status_str}{StatusEnum.PENDING.value}"

        if status_counts[StatusEnum.UNKNOWN] > 0:
            return f"{status_str}{StatusEnum.UNKNOWN.value}. Malformed status found."

        if status_counts[StatusEnum.FAILED] > 0:
            return (
                f"{status_str}{RED_UNSTABLE} "
                f"({status_counts[StatusEnum.FAILED]} shard(s) failed)"
            )

        return f"{status_str}{GREEN_RUNNING}"

    return status_str


def get_experiment_status_summary(runs: t.Optional[t.List[Run]]) -> str:
    """Get the status summary of an experiment

    Gets the status of each entity and returns
    a summary of the overall experiment.

    :param runs: Runs of an experiment
    :type runs: Optional[List[Run]]
    :return: Status summary
    :rtype: str
    """
    status_str = "Status: "

    if runs:
        apps = [app for run in runs for app in run.model]
        ensembles = [ensemble for run in runs for ensemble in run.ensemble]
        ens_members = [member for ensemble in ensembles for member in ensemble.models]
        orcs = [orch for run in runs for orch in run.orchestrator]
        shards = [shard for orc in orcs for shard in orc.shards]

        for entity in itertools.chain(apps, ens_members, shards):
            unknown_counter = 0
            try:
                entity_status = get_status(entity.telemetry_metadata["status_dir"])
            except KeyError:
                entity_status = StatusData(StatusEnum.UNKNOWN, None)
                unknown_counter += 1

            if entity_status in (
                StatusData(StatusEnum.RUNNING, None),
                StatusData(StatusEnum.PENDING, None),
            ):
                return f"{status_str}{GREEN_RUNNING}"

        if unknown_counter > 0:
            return f"{status_str}{StatusEnum.UNKNOWN.value}. Malformed status found."

        return f"{status_str}{StatusEnum.INACTIVE.value}"

    return status_str


def format_status(status: StatusData) -> str:
    """Format a status tuple

    :param status: Status enum and return code
    :type status: StatusData
    :return: Formatted status
    :rtype: str
    """
    status_str = "Status: "

    if status.status == StatusEnum.RUNNING:
        return f"{status_str}{GREEN_RUNNING}"
    if status.status == StatusEnum.COMPLETED:
        return f"{status_str}{GREEN_COMPLETED}"
    if status.status == StatusEnum.PENDING:
        return f"{status_str}{StatusEnum.PENDING.value}"
    if status.status == StatusEnum.FAILED:
        return f"{status_str}{RED_FAILED}"

    return f"{status_str}{StatusEnum.UNKNOWN.value}"


def status_mapping(
    entities: t.Union[t.List[Application], t.List[Shard]]
) -> t.Dict[StatusEnum, int]:
    """Map statuses for formatting

    :param entities: List of entities to map
    :type entities: Union[List[Application], List[Shard]]
    :return: The status map
    :rtype: Dict[StatusEnum, int]
    """
    status_counts = {
        StatusEnum.RUNNING: 0,
        StatusEnum.COMPLETED: 0,
        StatusEnum.FAILED: 0,
        StatusEnum.PENDING: 0,
        StatusEnum.UNKNOWN: 0,
    }

    for e in entities:
        try:
            entity_status = get_status(e.telemetry_metadata["status_dir"])
        except KeyError:
            entity_status = StatusData(StatusEnum.UNKNOWN, None)

        status_counts[entity_status.status] += 1

    return status_counts

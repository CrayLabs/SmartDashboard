import itertools
import json
import os
import typing as t
from dataclasses import dataclass

from .status import GREEN_COMPLETED, GREEN_RUNNING, RED_FAILED, RED_UNSTABLE, StatusEnum


@dataclass
class StatusData:
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
            with open(stop_json_path, "r", encoding="utf-8") as stop_json_file:
                stop_data = json.load(stop_json_file)

            return (
                StatusData(StatusEnum.FAILED, stop_data["return_code"])
                if stop_data["return_code"] != 0
                else StatusData(StatusEnum.COMPLETED, stop_data["return_code"])
            )

        return StatusData(StatusEnum.RUNNING, None)

    return StatusData(StatusEnum.PENDING, None)


def get_ensemble_status_summary(ensemble: t.Optional[t.Dict[str, t.Any]]) -> str:
    """Get the status summary of an ensemble

    Gets the status of each member and returns
    a summary of the overall ensemble.

    :param ensemble: Ensemble
    :type ensemble: t.Optional[t.Dict[str, t.Any]]
    :return: Status summary
    :rtype: str
    """
    status_str = "Status: "

    if ensemble:
        status_counts = status_mapping(ensemble.get("models", []))

        formatted_counts = [
            f"{count} {status.value}" for status, count in status_counts.items()
        ]

        status_description = f"{status_str}{', '.join(formatted_counts)}"

        return status_description

    return status_str


def get_orchestrator_status_summary(
    orchestrator: t.Optional[t.Dict[str, t.Any]]
) -> str:
    """Get the status summary of an orchestrator

    Gets the status of each shard and returns
    a summary of the overall orchestrator.

    :param orchestrator: Orchestrator
    :type orchestrator: t.Optional[t.Dict[str, t.Any]]
    :return: Status summary
    :rtype: str
    """
    status_str = "Status: "

    if orchestrator:
        status_counts = status_mapping(orchestrator.get("shards", []))

        if status_counts[StatusEnum.COMPLETED] == sum(status_counts.values()):
            return f"{status_str}{StatusEnum.INACTIVE} (all shards completed)"

        if status_counts[StatusEnum.PENDING] == sum(status_counts.values()):
            return f"{status_str}{StatusEnum.PENDING}"

        if status_counts[StatusEnum.FAILED] > 0:
            return (
                f"{status_str}{RED_UNSTABLE} "
                f"({status_counts[StatusEnum.FAILED]} shard(s) failed)"
            )

        return f"{status_str}{GREEN_RUNNING}"

    return status_str


def get_experiment_status_summary(runs: t.Optional[t.List[t.Dict[str, t.Any]]]) -> str:
    """Get the status summary of an experiment

    Gets the status of each entity and returns
    a summary of the overall experiment.

    :param runs: Runs of an experiment
    :type runs: t.Optional[t.List[t.Dict[str, t.Any]]]
    :return: Status summary
    :rtype: str
    """
    status_str = "Status: "

    if runs:
        apps = [app for run in runs for app in run.get("model", [])]
        ensembles = [ensemble for run in runs for ensemble in run.get("ensemble", [])]
        ens_members = [
            member for ensemble in ensembles for member in ensemble.get("models", [])
        ]
        orcs = [orch for run in runs for orch in run.get("orchestrator", [])]
        shards = [shard for orc in orcs for shard in orc.get("shards", [])]

        for entity in itertools.chain(apps, ens_members, shards):
            entity_status = get_status(entity["telemetry_metadata"]["status_dir"])
            if entity_status in (
                StatusData(StatusEnum.RUNNING, None),
                StatusData(StatusEnum.PENDING, None),
            ):
                return f"{status_str}{GREEN_RUNNING}"

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

    return f"{status_str}{RED_FAILED}"


def status_mapping(entities: t.List[t.Dict[str, t.Any]]) -> t.Dict[StatusEnum, int]:
    """Map statuses for formatting

    :param entities: List of entities to map
    :type entities: t.List
    :return: The status map
    :rtype: t.Dict[StatusEnum, int]
    """
    status_counts = {
        StatusEnum.RUNNING: 0,
        StatusEnum.COMPLETED: 0,
        StatusEnum.FAILED: 0,
        StatusEnum.PENDING: 0,
    }

    for e in entities:
        entity_status = get_status(e["telemetry_metadata"]["status_dir"])
        status_counts[entity_status.status] += 1

    return status_counts

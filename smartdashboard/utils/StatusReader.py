import json
import os
import typing as t

from .status import (
    GREEN_COMPLETED,
    GREEN_RUNNING,
    RED_FAILED,
    RED_INACTIVE,
    RED_UNSTABLE,
    STATUS_COMPLETED,
    STATUS_FAILED,
    STATUS_INACTIVE,
    STATUS_PENDING,
    STATUS_RUNNING,
)


def get_status(dir_path: str) -> t.Tuple[str, t.Optional[int]]:
    """Get the status of an application or shard

    This function is used to get the status of
    applications and shards. Status summary
    functions also use this to get the status
    of each of their members.

    :param dir_path: Directory of the entity
    :type dir_path: str
    :return: Status tuple (status category, return code)
    :rtype: t.Tuple[str, t.Optional[int]]
    """
    start_json_path = os.path.join(dir_path, "start.json")
    stop_json_path = os.path.join(dir_path, "stop.json")

    if os.path.exists(start_json_path):
        if os.path.exists(stop_json_path):
            with open(stop_json_path, "r", encoding="utf-8") as stop_json_file:
                stop_data = json.load(stop_json_file)

            return (
                (STATUS_FAILED, stop_data["return_code"])
                if stop_data["return_code"] != 0
                else (STATUS_COMPLETED, stop_data["return_code"])
            )

        return (STATUS_RUNNING, None)

    return (STATUS_PENDING, None)


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
        members = ensemble.get("models", [])

        status_counts = {
            STATUS_RUNNING: 0,
            STATUS_COMPLETED: 0,
            STATUS_FAILED: 0,
            STATUS_PENDING: 0,
        }

        for mem in members:
            mem_status = get_status(mem["telemetry_metadata"]["status_dir"])
            status_counts[mem_status[0]] += 1

        formatted_counts = [
            f"{count} {status}" for status, count in status_counts.items()
        ]

        status_description = status_str + ", ".join(formatted_counts)

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
        statuses = []
        shards = orchestrator.get("shards", [])

        status_counts = {
            STATUS_RUNNING: 0,
            STATUS_COMPLETED: 0,
            STATUS_FAILED: 0,
            STATUS_PENDING: 0,
        }

        for shard in shards:
            shard_status = get_status(shard["telemetry_metadata"]["status_dir"])
            statuses.append(shard_status)
            status_counts[shard_status[0]] += 1

        if status_counts[STATUS_COMPLETED] == len(statuses):
            return status_str + f"{STATUS_INACTIVE} (all shards completed)"

        if status_counts[STATUS_PENDING] == len(statuses):
            return status_str + f"{STATUS_PENDING}"

        if status_counts[STATUS_FAILED] > 0:
            return (
                status_str
                + f"{RED_UNSTABLE} ({status_counts[STATUS_FAILED]} shard(s) failed)"
            )

        return status_str + f"{GREEN_RUNNING}"

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
        for app in apps:
            app_status = get_status(app["telemetry_metadata"]["status_dir"])
            if app_status in ((STATUS_RUNNING, None), (STATUS_PENDING, None)):
                return status_str + f"{GREEN_RUNNING}"

        orcs = [orch for run in runs for orch in run.get("orchestrator", [])]
        for orc in orcs:
            shards = orc.get("shards", [])
            for shard in shards:
                shard_status = get_status(shard["telemetry_metadata"]["status_dir"])
                if shard_status in ((STATUS_RUNNING, None), (STATUS_PENDING, None)):
                    return status_str + f"{GREEN_RUNNING}"

        ensembles = [ensemble for run in runs for ensemble in run.get("ensemble", [])]
        for e in ensembles:
            members = e.get("models", [])
            for member in members:
                member_status = get_status(member["telemetry_metadata"]["status_dir"])
                if member_status in ((STATUS_RUNNING, None), (STATUS_PENDING, None)):
                    return status_str + f"{GREEN_RUNNING}"

        return status_str + f"{RED_INACTIVE}"

    return status_str


def format_status(status: t.Tuple[str, t.Optional[int]]) -> str:
    """Format a status tuple

    :param status: Status tuple
    :type status: t.Tuple[str, t.Optional[int]]
    :return: Formatted status
    :rtype: str
    """
    status_str = "Status: "

    if status[0] == STATUS_RUNNING:
        return status_str + f"{GREEN_RUNNING}"
    if status[0] == STATUS_COMPLETED:
        return status_str + f"{GREEN_COMPLETED}"
    if status[0] == STATUS_PENDING:
        return status_str + f"{STATUS_PENDING}"

    return status_str + f"{RED_FAILED} with exit code {status[1]}"

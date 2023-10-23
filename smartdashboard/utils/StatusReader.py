import json
import os
import typing as t


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
                ("Failed", stop_data["return_code"])
                if stop_data["return_code"] != 0
                else ("Completed", stop_data["return_code"])
            )

        return ("Running", None)

    return ("Pending", None)


def get_ensemble_status_summary(ensemble: t.Optional[t.Dict[str, t.Any]]) -> str:
    """Get the status summary of an ensemble

    Gets the status of each member and returns
    a summary of the overall ensemble.

    :param ensemble: Ensemble
    :type ensemble: t.Optional[t.Dict[str, t.Any]]
    :return: Status summary
    :rtype: str
    """
    if ensemble:
        members = ensemble.get("models", [])

        status_counts = {"Running": 0, "Completed": 0, "Failed": 0, "Pending": 0}

        for mem in members:
            mem_status = get_status(mem["telemetry_metadata"]["status_dir"])
            status_counts[mem_status[0]] += 1

        formatted_counts = [
            f"{count} {status}" for status, count in status_counts.items()
        ]

        status_description = "Status: " + ", ".join(formatted_counts)

        return status_description

    return "Status: "


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
    if orchestrator:
        statuses = []
        shards = orchestrator.get("shards", [])

        status_counts = {"Failed": 0, "Completed": 0, "Running": 0, "Pending": 0}

        for shard in shards:
            shard_status = get_status(shard["telemetry_metadata"]["status_dir"])
            statuses.append(shard_status)
            status_counts[shard_status[0]] += 1

        if status_counts["Completed"] == len(statuses):
            return "Status: Inactive (all shards completed)"

        if status_counts["Pending"] == len(statuses):
            return "Status: Pending"

        if status_counts["Failed"] > 0:
            return f'Status: :red[Unstable ({status_counts["Failed"]} shard(s) failed)]'

        return "Status: :green[Running]"

    return "Status: "


def get_experiment_status_summary(runs: t.Optional[t.List[t.Dict[str, t.Any]]]) -> str:
    """Get the status summary of an experiment

    Gets the status of each entity and returns
    a summary of the overall experiment.

    :param runs: Runs of an experiment
    :type runs: t.Optional[t.List[t.Dict[str, t.Any]]]
    :return: Status summary
    :rtype: str
    """
    if runs:
        apps = [app for run in runs for app in run.get("model", [])]
        for app in apps:
            app_status = get_status(app["telemetry_metadata"]["status_dir"])
            if app_status in (("Running", None), ("Pending", None)):
                return "Status: :green[Running]"

        orcs = [orch for run in runs for orch in run.get("orchestrator", [])]
        for orc in orcs:
            shards = orc.get("shards", [])
            for shard in shards:
                shard_status = get_status(shard["telemetry_metadata"]["status_dir"])
                if shard_status in (("Running", None), ("Pending", None)):
                    return "Status: :green[Running]"

        ensembles = [ensemble for run in runs for ensemble in run.get("ensemble", [])]
        for e in ensembles:
            members = e.get("models", [])
            for member in members:
                member_status = get_status(member["telemetry_metadata"]["status_dir"])
                if member_status in (("Running", None), ("Pending", None)):
                    return "Status: :green[Running]"

        return "Status: :red[Inactive]"

    return "Status: "


def format_status(status: t.Tuple[str, t.Optional[int]]) -> str:
    """Format a status tuple

    :param status: Status tuple
    :type status: t.Tuple[str, t.Optional[int]]
    :return: Formatted status
    :rtype: str
    """
    if status[0] == "Running":
        return "Status: :green[Running]"
    if status[0] == "Completed":
        return "Status: :green[Completed]"
    if status[0] == "Pending":
        return "Status: Pending"

    return f"Status: :red[Failed with exit code {status[1]}]"

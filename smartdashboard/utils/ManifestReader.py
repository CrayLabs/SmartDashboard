import io
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List

from smartdashboard.utils.errors import MalformedManifestError, ManifestError


@dataclass
class Manifest:
    experiment: Dict[str, Any]
    runs: List[Dict[str, Any]]
    applications: List[Dict[str, Any]]
    orchestrators: List[Dict[str, Any]]
    ensembles: List[Dict[str, Any]]


class ManifestReader(ABC):
    @abstractmethod
    def get_manifest(self) -> Manifest:
        ...


class ManifestFileReader(ManifestReader):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._data = self.from_file(self._file_path)

    def get_manifest(self) -> Manifest:
        """Get the Manifest from self._data

        :return: Manifest
        :rtype: Manifest
        """
        experiment = self._data.get("experiment", {})
        runs = self._data.get("runs", [])
        try:
            apps = [
                {**app, "run_id": run["run_id"]}
                for run in runs
                for app in run.get("model", [])
            ]
        except Exception as exc:
            raise MalformedManifestError(
                "Applications are malformed.", file=self._file_path, exception=exc
            ) from exc

        try:
            orcs = [
                {**orch, "run_id": run["run_id"]}
                for run in runs
                for orch in run.get("orchestrator", [])
            ]
        except Exception as exc:
            raise MalformedManifestError(
                "Orchestrators are malformed.", file=self._file_path, exception=exc
            ) from exc

        try:
            ensembles = [
                {**ensemble, "run_id": run["run_id"]}
                for run in runs
                for ensemble in run.get("ensemble", [])
            ]
        except Exception as exc:
            raise MalformedManifestError(
                "Ensembles are malformed.", file=self._file_path, exception=exc
            ) from exc

        return Manifest(
            experiment=experiment,
            runs=runs,
            applications=apps,
            orchestrators=orcs,
            ensembles=ensembles,
        )

    @classmethod
    def from_file(cls, file_path: str) -> Dict[str, Any]:
        """Initialize self._data

        :param file_path: File path of the manifest
        :type file_path: str
        :return: self._data
        :rtype: Dict[str, Any]
        """
        with open(file_path, encoding="utf-8") as file:
            return cls.from_io_stream(file)

    @classmethod
    def from_io_stream(cls, stream: io.TextIOBase) -> Dict[str, Any]:
        """Continue initializing self._data

        :param stream: io.TextIOBase to be decoded
        :type stream: io.TextIOBase
        :return: self._data
        :rtype: Dict[str, Any]
        """
        data: Dict[str, Any] = json.loads(stream.read())
        return data


def load_manifest(path: str) -> Manifest:
    """Instantiate and call get_manifest

    This is where we're checking for any errors
    that could occur when creating a manifest
    from file.

    :param path: Path to the manifest file
    :type path: str
    :return: Manifest
    :rtype: Optional[Manifest]
    """
    try:
        manifest_file_reader = ManifestFileReader(path)
        manifest = manifest_file_reader.get_manifest()
    except FileNotFoundError as fnf:
        raise ManifestError(
            title="Manifest file does not exist.", file=path, exception=fnf
        ) from fnf
    except json.decoder.JSONDecodeError as jde:
        raise ManifestError(
            title="Manifest file could not be decoded.", file=path, exception=jde
        ) from jde
    return manifest

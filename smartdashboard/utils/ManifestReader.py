import io
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from smartdashboard.utils.errors import MalformedManifestError


@dataclass
class Manifest:
    experiment: Optional[Dict[str, Any]]
    runs: List[Dict[str, Any]]
    applications: List[Dict[str, Any]]
    orchestrators: List[Dict[str, Any]]
    ensembles: List[Dict[str, Any]]


class ManifestReader(ABC):
    @abstractmethod
    def get_manifest(self) -> "Manifest":
        ...


class ManifestFileReader(ManifestReader):
    def __init__(self, file_path: str) -> None:
        self._file_path = file_path
        self._data = self.from_file(self._file_path)

    def get_manifest(self) -> "Manifest":
        experiment = self._data.get("experiment")
        runs = self._data.get("runs", [])
        try:
            apps = [app for run in runs for app in run.get("model", None) if app]
            if not isinstance(apps, list):
                raise TypeError
        except (KeyError, TypeError) as exc:
            raise MalformedManifestError("Applications are malformed.") from exc

        try:
            orcs = [
                orch for run in runs for orch in run.get("orchestrator", None) if orch
            ]
            if not isinstance(orcs, list):
                raise TypeError
        except (KeyError, TypeError) as exc:
            raise MalformedManifestError("Orchestrators are malformed.") from exc

        try:
            ensembles = [
                ensemble
                for run in runs
                for ensemble in run.get("ensemble", None)
                if ensemble
            ]
            if not isinstance(ensembles, list):
                raise TypeError
        except (KeyError, TypeError) as exc:
            raise MalformedManifestError("Ensembles are malformed.") from exc

        return Manifest(
            experiment=experiment,
            runs=runs,
            applications=apps,
            orchestrators=orcs,
            ensembles=ensembles,
        )

    @classmethod
    def from_file(cls, path: str) -> Dict[str, Any]:
        try:
            file = open(path, encoding="utf-8")
        except FileNotFoundError:
            raise FileNotFoundError(
                "The file passed into the dashboard could not be found."
            )
        return cls.from_io_stream(file)

    @classmethod
    def from_io_stream(cls, stream: io.TextIOBase) -> Dict[str, Any]:
        try:
            data = json.loads(stream.read())
        except json.decoder.JSONDecodeError:
            raise json.decoder.JSONDecodeError(
                "The file passed into the dashboard could not be decoded."
            )
        return data

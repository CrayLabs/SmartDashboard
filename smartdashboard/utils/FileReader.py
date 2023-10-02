import io
import json
import os
from typing import Any, Dict, List, Union

from smartdashboard.utils.errors import MalformedManifestError


class Manifest:
    def __init__(self, manifest: dict[str, Any]) -> None:
        self._data = manifest

    @property
    def experiment(self) -> Dict[str, Any]:
        return self._data.get("experiment")

    @property
    def runs(self) -> List[Dict[str, Any]]:
        return self._data.get("runs")

    @property
    def applications(self) -> List[Dict[str, Any]]:
        try:
            apps = [app for run in self.runs for app in run.get("model")]
            if not isinstance(apps, list):
                raise TypeError
            return apps
        except (KeyError, TypeError) as exc:
            raise MalformedManifestError("Applications are malformed.") from exc

    @property
    def orchestrators(self) -> List[Dict[str, Any]]:
        try:
            orcs = [orch for run in self.runs for orch in run.get("orchestrator")]
            if not isinstance(orcs, list):
                raise TypeError
            return orcs
        except (KeyError, TypeError) as exc:
            raise MalformedManifestError('Orchestrators are malformed.') from exc

    @property
    def ensembles(self) -> List[Dict[str, Any]]:
        try:
            ensembles = [
                ensemble for run in self.runs for ensemble in run.get("ensemble")
            ]
            if not isinstance(ensembles, list):
                raise TypeError
            return ensembles
        except (KeyError, TypeError) as exc:
            raise MalformedManifestError("Ensembles are malformed.") from exc

    @classmethod
    def from_file(cls, path: Union[str, os.PathLike[str]]) -> "Manifest":
        with open(path, encoding="utf-8") as file:
            return cls.from_io_stream(file)

    @classmethod
    def from_io_stream(cls, stream: io.TextIOBase) -> "Manifest":
        return cls(json.loads(stream.read()))

    @classmethod
    def create_empty_manifest(cls) -> "Manifest":
        return cls({"experiment": {}, "runs": []})

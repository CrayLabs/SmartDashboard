import io
import json
from typing import Any, Dict, List, Optional

from smartdashboard.utils.errors import MalformedManifestError


class Manifest:
    def __init__(self, manifest: Dict[str, Any]) -> None:
        self._data = manifest

    @property
    def experiment(self) -> Optional[Dict[str, Any]]:
        return self._data.get("experiment")

    @property
    def runs(self) -> List[Dict[str, Any]]:
        return self._data.get("runs", [])

    @property
    def applications(self) -> List[Dict[str, Any]]:
        try:
            apps = [app for run in self.runs for app in run.get("model", None) if app]
            if not isinstance(apps, list):
                raise TypeError
            return apps
        except (KeyError, TypeError) as exc:
            raise MalformedManifestError("Applications are malformed.") from exc

    @property
    def orchestrators(self) -> List[Dict[str, Any]]:
        try:
            orcs = [
                orch
                for run in self.runs
                for orch in run.get("orchestrator", None)
                if orch
            ]
            if not isinstance(orcs, list):
                raise TypeError
            return orcs
        except (KeyError, TypeError) as exc:
            raise MalformedManifestError("Orchestrators are malformed.") from exc

    @property
    def ensembles(self) -> List[Dict[str, Any]]:
        try:
            ensembles = [
                ensemble
                for run in self.runs
                for ensemble in run.get("ensemble", None)
                if ensemble
            ]
            if not isinstance(ensembles, list):
                raise TypeError
            return ensembles
        except (KeyError, TypeError) as exc:
            raise MalformedManifestError("Ensembles are malformed.") from exc

    @classmethod
    def from_file(cls, path: str) -> "Manifest":
        with open(path, encoding="utf-8") as file:
            return cls.from_io_stream(file)

    @classmethod
    def from_io_stream(cls, stream: io.TextIOBase) -> "Manifest":
        return cls(json.loads(stream.read()))

    @classmethod
    def create_empty_manifest(cls) -> "Manifest":
        return cls({"experiment": {}, "runs": []})

import json
import io
import os
from typing import Any, Union, Dict, List


class Manifest:
    def __init__(self, manifest: dict[str, Any]) -> None:
        self._data = manifest

    @property
    def experiment(self) -> Dict[str, Any]:
        return self._data.get("experiment", {})

    @property
    def runs(self) -> List[Dict[str, Any]]:
        return self._data.get("runs", [])

    @property
    def applications(self) -> List[Dict[str, Any]]:
        return [app for run in self.runs for app in run.get("model", [])]

    @property
    def orchestrators(self) -> List[Dict[str, Any]]:
        return [orch for run in self.runs for orch in run.get("orchestrator", [])]

    @property
    def ensembles(self) -> List[Dict[str, Any]]:
        return [ensemble for run in self.runs for ensemble in run.get("ensemble", [])]

    @classmethod
    def from_file(cls, path: Union[str, os.PathLike[str]]) -> "Manifest":
        try:
            with open(path) as f:
                return cls.from_io_stream(f)
        except FileNotFoundError:
            return cls.create_empty_manifest()

    @classmethod
    def from_io_stream(cls, stream: io.TextIOBase) -> "Manifest":
        return cls(json.loads(stream.read()))

    @classmethod
    def create_empty_manifest(cls) -> "Manifest":
        return cls({"experiment": {}, "runs": []})

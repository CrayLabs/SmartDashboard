import json
import io
import os
from typing import Any, Union


class ManifestReader:
    def __init__(self, manifest: dict[str, Any]) -> None:
        self._data = manifest

    @property
    def experiment(self):
        return self._data.get("experiment")

    @property
    def runs(self):
        return self._data.get("runs")

    @property
    def applications(self):
        return [app for run in self.runs for app in run.get("model", [])]

    @property
    def orchestrators(self):
        return [orch for run in self.runs for orch in run.get("orchestrator", [])]

    @property
    def ensembles(self):
        return [ensemble for run in self.runs for ensemble in run.get("ensemble", [])]

    @classmethod
    def from_file(cls, path: Union[str, os.PathLike[str]]) -> "ManifestReader":
        try:
            with open(path) as f:
                return cls.from_io_stream(f)
        except FileNotFoundError:
            return cls.create_empty_manifest()

    @classmethod
    def from_io_stream(cls, stream: io.TextIOBase) -> "ManifestReader":
        return cls(json.loads(stream.read()))

    @classmethod
    def create_empty_manifest(cls) -> "ManifestReader":
        return cls({"experiment": {}, "runs": []})

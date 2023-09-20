import json
from typing import List, Dict, Any, Optional


class ManifestReader:
    def __init__(self, filename: str):
        self.filename = filename
        self.data: Optional[Dict[str, Any]] = None
        self.experiment: Dict[str, str] = {}
        self.runs: List[Dict[str, Any]] = []
        self.applications: List[Dict[str, Any]] = []
        self.orchestrators: List[Dict[str, Any]] = []
        self.ensembles: List[Dict[str, Any]] = []
        self.load_data()

    def load_data(self) -> None:
        """
        Processes the JSON data into lists of entities.
        """
        try:
            with open(self.filename, "r", encoding="utf-8") as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            self.data = None
            self.experiment = {}
            return

        if self.data is not None:
            self.experiment = self.data.get("experiment", {})
            self.runs = self.data.get("runs", [])
            self.applications = [
                app for run in self.runs for app in run.get("model", [])
            ]
            self.orchestrators = [
                orch for run in self.runs for orch in run.get("orchestrator", [])
            ]
            self.ensembles = [
                ensemble for run in self.runs for ensemble in run.get("ensemble", [])
            ]

    def get_entity(
        self, entity_name: str, entity_list: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Gets an entity from a list of entities when you only
        know its name.

        Args:
            entity_name (str): The name of the entity to search for. This is
            gotten from a dropdown in the dashboard.
            entity_list (List[Dict[str, Any]]): The list of entites
            to search through.

        Returns:
            Optional[Dict[str, Any]]: If found, returns the entity.
            Otherwise returns None.
        """
        if self.data is None:
            return None
        for entity in entity_list:
            if entity and "name" in entity and entity["name"] == entity_name:
                return entity
        return None

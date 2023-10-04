from typing import Any, Dict, List, Optional, Tuple, Union


def get_value(key: str, entity: Optional[Dict[str, Any]]) -> str:
    """Get the value of a key-value pair

    :param key: Key of the dictionary
    :type key: str
    :param entity: Entity represented by a dictionary
    :type entity: Optional[Dict[str, Any]]
    :return: Value of the key-value pair
    :rtype: str
    """
    if entity:
        return entity.get(key, "")

    return ""


def get_exe_args(entity: Optional[Dict[str, Any]]) -> List[str]:
    """Get the exe_args of an entity

    :param entity: Entity represented by a dictionary
    :type entity: Optional[Dict[str, Any]]
    :return: exe_args of the entity
    :rtype: List[str]
    """
    if entity:
        return entity.get("exe_args", [])

    return []


def get_interfaces(entity: Optional[Dict[str, Any]]) -> str:
    """Get and format the interfaces of an entity

    :param entity: Entity represented by a dictionary
    :type entity: Optional[Dict[str, Any]]
    :return: Interfaces
    :rtype: str
    """
    if entity:
        value: str = entity.get("interface", "")
        if isinstance(value, List):
            return ", ".join(value)
        return value

    return ""


def get_ensemble_members(
    ensemble: Optional[Dict[str, Any]]
) -> List[Optional[Dict[str, Any]]]:
    """Get the members of an ensemble

    :param ensemble: Ensemble represented by a dictionary
    :type ensemble: Optional[Dict[str, Any]]
    :return: All members of the ensemble
    :rtype: List[Optional[Dict[str, Any]]]
    """
    if ensemble:
        return ensemble.get("models", [])

    return []


def get_member(
    member_name: str, ensemble: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Get a specific member of an ensemble

    :param member_name: Name of the selected member
    :type member_name: str
    :param ensemble: Ensemble represented by a dictionary
    :type ensemble: Optional[Dict[str, Any]]
    :return: Selected member
    :rtype: Optional[Dict[str, Any]]
    """
    for member in get_ensemble_members(ensemble):
        if member and "name" in member and member["name"] == member_name:
            return member

    return None


def get_port(orc: Optional[Dict[str, Any]]) -> str:
    """Get the port of an orchestrator

    The ports in all of the shards should be the same.

    :param orc: Orchestrator represented by a dictionary
    :type orc: Optional[Dict[str, Any]]
    :return: Port
    :rtype: str
    """
    shard_ports = set()

    if orc:
        for shard in orc.get("shards", []):
            port = str(shard.get("port"))
            if port:
                shard_ports.add(port)

        if len(shard_ports) == 1:
            return shard_ports.pop()

        raise Exception("Shards within an Orchestrator should have the same port.")

    return ""


def get_db_hosts(orc: Optional[Dict[str, Any]]) -> List[str]:
    """Get the db_hosts of an orchestrator

    The hosts of all of the shards are displayed.

    :param orc: Orchestrator represented by a dictionary
    :type orc: Optional[Dict[str, Any]]
    :return: Hosts
    :rtype: List[str]
    """
    hosts = []

    if orc:
        for shard in orc.get("shards", []):
            host = shard.get("host")
            if host:
                hosts.append(host)

    return hosts


def flatten_nested_keyvalue_containers(
    dict_name: str, entity: Optional[Dict[str, Any]]
) -> List[Tuple[str, str]]:
    """Format dicts of all types to be displayed

    The dictionaries can have a combination of types attached, so
    displaying each item within the dict needs to be checked by type
    and handled correctly.

    :param dict_name: Name of the dictionary
    :type dict_name: str
    :param entity: Entity represented by a dictionary
    :type entity: Optional[Dict[str, Any]]
    :return: (keys, values) list
    :rtype: List[Tuple[str,str]]
    """
    keys = []
    values = []

    if entity:
        target_dict = entity.get(dict_name, {})
        for key, value in target_dict.items():
            if isinstance(value, List):
                for val in value:
                    keys.append(key)
                    values.append(str(val))
            elif isinstance(value, Dict):
                for k, v in value.items():
                    keys.append(k)
                    values.append(str(v))
            else:
                keys.append(key)
                values.append(str(value))

    return list(zip(keys, values))


def format_ensemble_params(entity: Optional[Dict[str, Any]]) -> List[Tuple[str, str]]:
    """Format ensemble params to be displayed

    :param entity: Entity represented by a dictionary
    :type entity: Optional[Dict[str, Any]]
    :return: (keys, values) list
    :rtype: List[Tuple[str,str]]
    """
    keys = []
    values = []

    if entity:
        target_dict = entity.get("params", {})
        for key, value in target_dict.items():
            comma_separated_string = ", ".join(value)
            keys.append(key)
            values.append(comma_separated_string)

    return list(zip(keys, values))


def get_loaded_entities(
    entity: Optional[Dict[str, Any]]
) -> Union[List[Dict[str, str]], Dict[str, List[Any]]]:
    """Combine and format loaded entities

    DB Models and DB Scripts are combined so they can be displayed as
    "Loaded Entities" in the dashboard.

    :param entity: Entity represented by a dictionary
    :type entity: Optional[Dict[str, Any]]
    :return: A list of formatted loaded entity dicts, or one formatted dict
    :rtype: Union[List[Dict[str, str]], Dict[str, List[Any]]]
    """
    loaded_data = []
    if entity:
        for item in entity.get("models", []):
            for key, value in item.items():
                loaded_data.append(
                    {
                        "Name": key,
                        "Type": "DB Model",
                        "Backend": value["backend"],
                        "Device": value["device"],
                    }
                )
        for item in entity.get("scripts", []):
            for key, value in item.items():
                loaded_data.append(
                    {
                        "Name": key,
                        "Type": "DB Script",
                        "Backend": value["backend"],
                        "Device": value["device"],
                    }
                )

        if not loaded_data:
            return {"Name": [], "Type": [], "Backend": [], "Device": []}
        return loaded_data

    return {"Name": [], "Type": [], "Backend": [], "Device": []}


def get_entities_with_name(
    entity_name: str, entity_list: List[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """Get a specific entity from a list of entities

    :param entity_name: Name of the entity
    :type entity_name: str
    :param entity_list: List of entities to search through
    :type entity_list: List[Dict[str, Any]]
    :return: Entity represented by a dictionary
    :rtype: Optional[Dict[str, Any]]
    """
    entities: List[Dict[str, Any]] = [
        e for e in entity_list if entity_name == e["name"]
    ]

    if entities:
        return entities[0]

    return None

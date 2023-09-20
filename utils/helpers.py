from typing import List, Tuple, Dict, Any, Optional, Union


def get_value(key: str, entity: Optional[Dict[str, Any]]) -> str:
    """
    Gets the value of the key-value pair. Returns an empty string
    if entity is None for dashboard displaying purposes.
    """
    if entity:
        return entity.get(key, "")

    return ""


def get_exe_args(entity: Optional[Dict[str, Any]]) -> List[str]:
    """
    Gets the exe_args of the entity. Returns an empty list
    if entity is None for dashboard displaying purposes.
    """
    if entity:
        return entity.get("exe_args", [])

    return []


def get_interface(entity: Optional[Dict[str, Any]]) -> str:
    """
    Gets and formats the interface(s) of the entity. Returns an empty
    string if entity is None for dashboard displaying purposes.
    """
    if entity:
        value = entity.get("interface", "")
        if isinstance(value, List):
            return ", ".join(value)
        return value

    return ""


def get_ensemble_members(
    ensemble: Optional[Dict[str, Any]]
) -> List[Optional[Dict[str, Any]]]:
    """
    Gets all of the members inside of an ensemble. Returns an empty
    list if entity is None for dashboard displaying purposes.
    """
    if ensemble:
        return ensemble.get("models", [])

    return []


def get_member(
    member_name: str, ensemble: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    """
    Gets a specific member from an ensemble. Returns None if not found.
    """
    for member in get_ensemble_members(ensemble):
        if member and "name" in member and member["name"] == member_name:
            return member

    return None


def get_port(orc: Optional[Dict[str, Any]]) -> str:
    """
    Gets the port to display for the Orchestrator. The ports within
    the shards should be the same, otherwise raise an exception.
    Return empty string if entity is None for displaying purposes.
    """
    shard_ports = set()

    if orc:
        for shard in orc.get("shards", []):
            port = str(shard.get("port"))
            if port:
                shard_ports.add(port)

        if len(shard_ports) == 1:
            return shard_ports.pop()
        else:
            raise Exception("Shards within an Orchestrator should have the same port.")

    return ""


def get_db_hosts(orc: Optional[Dict[str, Any]]) -> List[str]:
    """
    Gets the db_hosts to display for the Orchestrator. The hosts within
    the shards are gathered and displayed.
    Return empty list if entity is None for displaying purposes.
    """
    hosts = []

    if orc:
        for shard in orc.get("shards", []):
            host = shard.get("host")
            if host:
                hosts.append(host)

    return hosts


def format_mixed_nested_dict(
    dict_name: str, entity: Optional[Dict[str, Any]]
) -> Tuple[List[str], List[str]]:
    """
    Formats dicts in order to properly display them in the dashboard.
    The dictionaries can have a combination of types attached, so
    displaying each item within the dict needs to be checked by type
    and handled correctly.
    """
    keys = []
    values = []

    if entity:
        dict = entity.get(dict_name, {})
        for key, value in dict.items():
            if isinstance(value, List):
                for v in value:
                    keys.append(key)
                    values.append(str(v))
            elif isinstance(value, Dict):
                for k, v in value.items():
                    keys.append(k)
                    values.append(str(v))
            else:
                keys.append(key)
                values.append(str(value))

    return keys, values


def format_ensemble_params(
    entity: Optional[Dict[str, Any]]
) -> Tuple[List[str], List[str]]:
    """
    Formats ensemble params in order to properly display them in the dashboard.
    """
    keys = []
    values = []

    if entity:
        target_dict = entity.get("params", {})
        for key, value in target_dict.items():
            comma_separated_string = ", ".join(value)
            keys.append(key)
            values.append(comma_separated_string)

    return keys, values


def get_loaded_entities(
    entity: Optional[Dict[str, Any]]
) -> Union[List[Dict[str, str]], Dict[str, List[Any]]]:
    """
    This function properly combines and formats the keys and values of
    DB Models and DB Scripts so they can be displayed as "Loaded Entities"
    in the dashboard.

    Args:
        entity (Optional[Dict[str, Any]]): The entity we get DB Models
        and Db Scripts from.

    Returns:
        Union[List[Dict[str,str]], Dict[str, List[Any]]]: Returns a list of dicts
        with Name, Type, Backend, and Device as the keys. If there are no DB
        Models or DB Scripts, or the entity passed in doesn't exist, this function
        returns a single dict with the headers for the table and empty lists as
        their values. The dashboard displays that there is no data when this is
        done.
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

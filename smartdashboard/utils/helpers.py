# BSD 2-Clause License
#
# Copyright (c) 2021-2023, Hewlett Packard Enterprise
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import typing as t

import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator

from smartdashboard.schemas.application import Application
from smartdashboard.schemas.base import BaseEntity
from smartdashboard.schemas.ensemble import Ensemble
from smartdashboard.schemas.orchestrator import Orchestrator
from smartdashboard.schemas.shard import Shard


def get_interfaces(entity: t.Optional[Orchestrator]) -> str:
    """Get and format the interfaces of an entity

    :param entity: Orchestrator
    :type entity: Optional[Orchestrator]
    :return: Interfaces of the orchestrator
    :rtype: str
    """
    if entity:
        value = entity.interface
        if isinstance(value, list):
            return ", ".join(value)
        return value

    return ""


def get_ensemble_members(ensemble: t.Optional[Ensemble]) -> t.List[Application]:
    """Get the members of an ensemble

    :param ensemble: Ensemble
    :type ensemble: Optional[Ensemble]
    :return: All members of the ensemble
    :rtype: List[Application]
    """
    if ensemble:
        return list(ensemble.models)

    return []


def get_member(
    member_name: str, ensemble: t.Optional[Ensemble]
) -> t.Optional[Application]:
    """Get a specific member of an ensemble

    :param member_name: Name of the selected member
    :type member_name: str
    :param ensemble: Ensemble
    :type ensemble: Optional[Ensemble]
    :return: Selected member
    :rtype: Optional[Application]
    """
    for member in get_ensemble_members(ensemble):
        if member.name == member_name:
            return member

    return None


def get_port(orc: t.Optional[Orchestrator]) -> str:
    """Get the port of an orchestrator

    The ports in all of the shards should be the same.

    :param orc: Orchestrator
    :type orc: Optional[Orchestrator]
    :return: Port
    :rtype: str
    """
    shard_ports = set()

    if orc:
        for shard in orc.shards:
            port = str(shard.port)
            if port:
                shard_ports.add(port)

        if len(shard_ports) == 1:
            return shard_ports.pop()

        return (
            "Warning! Shards within an Orchestrator should have the same port. "
            + ", ".join(sorted(shard_ports))
        )

    return ""


def get_db_hosts(orc: t.Optional[Orchestrator]) -> t.List[str]:
    """Get the db_hosts of an orchestrator

    The hosts of all of the shards are displayed.

    :param orc: Orchestrator
    :type orc: Optional[Orchestrator]
    :return: Hosts
    :rtype: List[str]
    """
    hosts = []

    if orc:
        for shard in orc.shards:
            host = shard.hostname
            if host:
                hosts.append(host)

    return hosts


def flatten_nested_keyvalue_containers(
    dict_name: str,
    entity: t.Union[t.Optional[t.Dict[str, t.Any]], t.Optional[BaseEntity]],
) -> t.List[t.Tuple[str, str]]:
    """Format dicts of all types to be displayed

    The dictionaries can have a combination of types attached, so
    displaying each item within the dict needs to be checked by type
    and handled correctly.

    :param dict_name: Name of the dictionary
    :type dict_name: str
    :param entity: Entity represented by a dictionary or a BaseEntity
    :type entity: Union[Optional[Dict[str, Any]], Optional[BaseEntity]]
    :return: (keys, values) list
    :rtype: List[Tuple[str,str]]
    """
    keys = []
    values = []

    if entity:
        if isinstance(entity, BaseEntity):
            target_dict = getattr(entity, dict_name, {})
        else:
            target_dict = entity.get(dict_name, {})
        for key, value in target_dict.items():
            if isinstance(value, list):
                for val in value:
                    keys.append(key)
                    values.append(str(val))
            elif isinstance(value, dict):
                for k, v in value.items():
                    keys.append(k)
                    values.append(str(v))
            else:
                keys.append(key)
                values.append(str(value))

    return list(zip(keys, values))


def format_ensemble_params(entity: t.Optional[Ensemble]) -> t.List[t.Tuple[str, str]]:
    """Format ensemble params to be displayed

    :param entity: Ensemble
    :type entity: Optional[Ensemble]
    :return: (keys, values) list
    :rtype: List[Tuple[str,str]]
    """
    keys = []
    values = []

    if entity:
        target_dict = entity.params
        for key, value in target_dict.items():
            comma_separated_string = ", ".join(value)
            keys.append(key)
            values.append(comma_separated_string)

    return list(zip(keys, values))


def get_loaded_entities(
    colocated_dict: t.Optional[t.Dict[str, t.Any]]
) -> t.Union[t.List[t.Dict[str, str]], t.Dict[str, t.List[t.Any]]]:
    """Combine and format loaded entities

    DB Models and DB Scripts are combined so they can be displayed as
    "Loaded Entities" in the dashboard.

    :param colocated_dict: Colocated database dictionary within an Application
    :type colocated_dict: Optional[Dict[str, Any]]
    :return: A list of formatted loaded entity dicts, or one formatted dict
    :rtype: Union[List[Dict[str, str]], Dict[str, List[Any]]]
    """
    loaded_data = []
    if colocated_dict:
        for item in colocated_dict.get("models", []):
            for key, value in item.items():
                loaded_data.append(
                    {
                        "Name": key,
                        "Type": "DB Model",
                        "Backend": value["backend"],
                        "Device": value["device"],
                    }
                )
        for item in colocated_dict.get("scripts", []):
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


def get_entity_from_name(
    entity_name: str, entity_list: t.Sequence[BaseEntity]
) -> t.Optional[BaseEntity]:
    """Get a specific entity from a list of entities

    :param entity_name: Name of the entity
    :type entity_name: str
    :param entity_list: Sequence of entities to search through
    :type entity_list: Sequence[BaseEntity]
    :return: Entity
    :rtype: Optional[BaseEntity]
    """
    return next(
        (e for e in entity_list if entity_name == f"{e.name}: Run {e.run_id}"),
        None,
    )


def build_dataframe_generic(
    column: DeltaGenerator,
    title: str,
    dict_name: str,
    entity: t.Union[t.Optional[t.Dict[str, t.Any]], t.Optional[BaseEntity]],
    df_columns: t.List[str],
) -> None:
    """Renders dataframe within a column

    :param column: Column the dataframe will be rendered in
    :type column: DeltaGenerator
    :param title: Title of the dataframe
    :type title: str
    :param dict_name: Name of the dictionary
    :type dict_name: str
    :param entity: Entity or dictionary being rendered
    :type entity: Union[Optional[Dict[str, Any]], Optional[BaseEntity]]
    :param df_columns: Dataframe column names
    :type df_columns: List[str]
    """
    with column:
        render_dataframe(
            title=title,
            dataframe=pd.DataFrame(
                flatten_nested_keyvalue_containers(dict_name, entity),
                columns=df_columns,
            ),
        )


def build_dataframe_loaded_entities(
    column: DeltaGenerator, title: str, colocated_dict: t.Optional[t.Dict[str, t.Any]]
) -> None:
    """Renders dataframe within a column

    Loaded entity information is collected
    differently, which is why there are two
    building functions.

    :param column: Column the dataframe will be rendered in
    :type column: DeltaGenerator
    :param title: Title of the dataframe
    :type title: str
    :param colocated_dict: Colocated database dictionary within an Application
    :type colocated_dict: Optional[Dict[str, Any]]
    """
    with column:
        render_dataframe(
            title=title,
            dataframe=pd.DataFrame(get_loaded_entities(colocated_dict)),
        )


def render_dataframe(dataframe: pd.DataFrame, title: t.Optional[str] = None) -> None:
    """Renders dataframe with optional titles

    :param title: Title of the dataframe
    :type title: Optional[str]
    :param dataframe: Dataframe to be rendered
    :type dataframe: pandas.Dataframe
    """
    if title:
        st.write(title)
    st.dataframe(
        dataframe,
        hide_index=True,
        use_container_width=True,
    )


def get_all_shards(orc: t.Optional[Orchestrator]) -> t.List[Shard]:
    """Get all shards in an Orchestrator

    :param orc: Orchestrator
    :type orc: Optional[Orchestrator]
    :return: List of shards
    :rtype: List[Shard]
    """
    if orc:
        return list(orc.shards)

    return []


def get_shard(shard_name: str, orc: t.Optional[Orchestrator]) -> t.Optional[Shard]:
    """Get a specific shard from an Orchestrator

    :param shard_name: Name of shard selected
    :type shard_name: str
    :param orc: Orchestrator
    :type orc: Optional[Orchestrator]
    :return: Selected shard
    :rtype: Optional[Shard]
    """
    for shard in get_all_shards(orc):
        if shard.name == shard_name:
            return shard

    return None


def shard_log_spacing() -> None:
    """Adds the necessary spacing to the
    error logs so they are even with the
    output logs for shards.
    """
    st.write("#")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

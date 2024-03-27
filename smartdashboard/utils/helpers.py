# BSD 2-Clause License
#
# Copyright (c) 2021-2024, Hewlett Packard Enterprise
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
from smartdashboard.schemas.ensemble import Ensemble
from smartdashboard.schemas.orchestrator import Orchestrator


def get_port(orc: t.Optional[Orchestrator]) -> str:
    """Get the port of an orchestrator

    The ports in all of the shards should be the same.

    :param orc: Orchestrator
    :type orc: Optional[Orchestrator]
    :return: Port
    :rtype: str
    """

    if orc:
        if len(orc.ports) == 1:
            return str(orc.ports[0])

        return (
            "Warning! Shards within an Orchestrator should have the same port. "
            + ", ".join(map(str, sorted(orc.ports)))
        )

    return ""


def format_interfaces(orc: t.Optional[Orchestrator]) -> str:
    """Format the interfaces of an orchestrator

    :param orc: Orchestrator
    :type orc: Optional[Orchestrator]
    :return: Formatted interfaces
    :rtype: str
    """

    if orc:
        return ", ".join(orc.interface)

    return ""


def flatten_nested_keyvalue_containers(
    dict_name: str,
    entity: t.Optional[t.Dict[str, t.Any]],
) -> t.List[t.Tuple[str, str]]:
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

    if entity is not None:
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


def build_dataframe_generic(
    column: DeltaGenerator,
    title: str,
    dict_name: str,
    entity: t.Optional[t.Dict[str, t.Any]],
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
    :type entity: Optional[Dict[str, Any]]
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
    column: DeltaGenerator, title: str, entity: t.Optional[Application]
) -> None:
    """Renders dataframe within a column

    Loaded entity information is collected
    differently, which is why there are two
    building functions.

    :param column: Column the dataframe will be rendered in
    :type column: DeltaGenerator
    :param title: Title of the dataframe
    :type title: str
    :param entity: Application to get loaded entities from
    :type entity: Application
    """
    with column:
        render_dataframe(
            title=title,
            dataframe=pd.DataFrame(
                entity.loaded_entities
                if entity is not None
                else {"Name": [], "Type": [], "Backend": [], "Device": []}
            ),
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

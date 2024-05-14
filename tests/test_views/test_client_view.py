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

import random

import pandas as pd
import pytest
import streamlit as st

from smartdashboard.views import ClientView, Files
from tests.utils.test_entities import *


@pytest.mark.parametrize(
    "shard, csv_length, telem_bool, files_tuple",
    [
        pytest.param(
            orchestrator_2.shards[0],
            30,
            True,
            Files(
                "tests/utils/clients/client_counts.csv",
                "tests/utils/clients/client.csv",
            ),
        ),
        pytest.param(telemetry_off_shard, 0, False, Files("", "")),
        pytest.param(
            telemetry_files_not_found, 0, False, Files("bad_file", "not_real")
        ),
    ],
)
def test_client_view(shard, csv_length, telem_bool, files_tuple):
    view = ClientView(
        shard,
        table_element=st.empty(),
        graph_element=st.empty(),
        export_button=st.empty(),
    )
    assert view.telemetry == telem_bool
    assert view.message == f"Client information could not be found for {shard.name}"
    assert view.columns == ["timestamp", "num_clients"]
    assert view.files == files_tuple
    if telem_bool:
        assert view.telemetry_df.shape[0] == csv_length

        assert list(view.telemetry_df.columns) == [
            "timestamp",
            "num_clients",
        ]
        assert view._get_data_file() != ""
    else:
        assert view._get_data_file() == ""


@pytest.mark.parametrize(
    "shard, csv_length",
    [
        pytest.param(orchestrator_2.shards[0], 30),
        pytest.param(telemetry_off_shard, 0),
        pytest.param(telemetry_files_not_found, 0),
    ],
)
def test_load_data_client_view(shard, csv_length):
    view = ClientView(
        shard,
        table_element=st.empty(),
        graph_element=st.empty(),
        export_button=st.empty(),
    )
    assert len(view._load_data_update(0)) == csv_length


@pytest.mark.parametrize(
    "shard, csv_length",
    [
        pytest.param(orchestrator_2.shards[0], 30),
    ],
)
def test_load_data_update_client_view(shard, csv_length):
    view = ClientView(
        shard,
        table_element=st.empty(),
        graph_element=st.empty(),
        export_button=st.empty(),
    )
    first_chunk = random.randint(1, csv_length - 1)
    initial_df = pd.read_csv(view.files.graph_file, nrows=first_chunk)
    df_delta = view._load_data_update(skiprows=initial_df.shape[0] + 1)
    assert pd.concat((initial_df, df_delta), axis=0).shape[0] == csv_length

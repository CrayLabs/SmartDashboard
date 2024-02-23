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

import pytest
import streamlit as st
import pandas as pd
import random

from smartdashboard.views import ClientView
from tests.utils.test_entities import *


@pytest.mark.parametrize(
    "shard, csv_length, telem_bool",
    [
        pytest.param(
            orchestrator_2.shards[0], 300, True
        ),
        pytest.param(
            telemetry_off_shard, 0, False
        ),
        pytest.param(
            telemetry_files_not_found, 0, False
        ),
    ],
)
def test_client_view(
    shard, csv_length, telem_bool
):
    view = ClientView(shard, table_element=st.empty(), graph_element=st.empty(), export_button=st.empty())
    assert view.telemetry == telem_bool
    if telem_bool:
        assert view.telemetry_df.shape[0] == csv_length
        
        assert list(view.telemetry_df.columns)==[
                'timestamp',
                "num_clients",
            ]
        assert view._get_data_file() != ""
    else:
        assert view._get_data_file() == ""


@pytest.mark.parametrize(
    "shard, csv_length",
    [
        pytest.param(
            orchestrator_2.shards[0], 300
        ),
        pytest.param(
            telemetry_off_shard, 0
        ),
        pytest.param(
            telemetry_files_not_found, 0
        ),
    ],
)
def test_load_data_client_view(
    shard, csv_length
):
    view = ClientView(shard, table_element=st.empty(), graph_element=st.empty(), export_button=st.empty())
    assert len(view._load_data()) == csv_length


@pytest.mark.parametrize(
    "shard, csv_length",
    [
        pytest.param(
            orchestrator_2.shards[0], 300
        ),
    ],
)
def test_load_data_update_client_view(
    shard, csv_length
):
    view = ClientView(shard, table_element=st.empty(), graph_element=st.empty(), export_button=st.empty())
    df = pd.read_csv(view.files[0], nrows=int(csv_length/2))
    first_chunk = random.randint(1,df.shape[0])
    initial_df = pd.read_csv(view.files[0], nrows=first_chunk)
    df_delta = view._load_data_update(skiprows=initial_df.shape[0]+1)
    assert pd.concat((initial_df, df_delta), axis=0).shape[0] == csv_length
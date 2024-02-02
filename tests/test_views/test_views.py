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

import pathlib
import pytest
import typing as t
import pandas as pd

from smartdashboard.views import load_data, _load_data

CsvGeneratorFunc = t.Callable[[int, int], pathlib.Path]


@pytest.fixture
def create_random_csv() -> CsvGeneratorFunc:
    """Parameterized fixture for generating CSV data for testing"""

    def _create_random_csv(num_rows: int = 3, num_cols: int = 2) -> pathlib.Path:
        """Generate a random test dataset and write to a file.
        :returns: The path to the test file"""
        txt = ""
        for i in range(num_rows):
            numbers = [str(i)] * num_cols
            txt += ",".join(numbers) + "\n"

        csv_path = pathlib.Path("test.csv")

        with open(str(csv_path), mode="w", encoding="utf-8") as fp:
            fp.write(txt)

        return csv_path

    return _create_random_csv


def test_load_clients(create_random_csv: CsvGeneratorFunc):
    """Ensure that csv loading returns a dataframe as expected"""
    csv_path = create_random_csv()
    df = _load_data(csv_path, start_idx=0, num_rows=3, has_header=False)

    assert df is not None
    assert df.shape[0] > 0


def test_load_clients_bad_path(create_random_csv: CsvGeneratorFunc):
    """Ensure that csv loading raises an exception when an invalid path is passed"""
    faux_csv = create_random_csv().with_stem("invalid_name")

    with pytest.raises(ValueError):
        _load_data(faux_csv, start_idx = 0, num_rows=5, has_header=False)


def test_iterative_dataload_full_file(create_random_csv: CsvGeneratorFunc):
    """Ensure that a csv containing fewer than MAX_RECORDS is loaded in a single step"""
    csv_path = create_random_csv()

    df_iterative, next_index = load_data(csv_path, 0)

    assert df_iterative.shape[0] > 0
    assert next_index == 0


def test_iterative_dataload_full_file(create_random_csv: CsvGeneratorFunc):
    """Ensure that a csv containing fewer than MAX_RECORDS is loaded in a single step"""
    csv_path = create_random_csv()

    df_iterative, next_index = load_data(csv_path, 0)

    assert df_iterative.shape[0] > 0
    assert next_index == 0


def test_iterative_dataload_partial_file(create_random_csv: CsvGeneratorFunc):
    """Ensure that a csv containing MORE than MAX_RECORDS is loaded in multiple steps"""
    csv_path = create_random_csv()

    df_iterative, next_index = load_data(csv_path, 0, num_rows=2)

    assert df_iterative.shape[0] == 2
    assert next_index == 2


@pytest.mark.parametrize(
    "num_rows,num_cols,next_index,max_records",
    [
        pytest.param(3, 2, [0], 4, id="exact final match, full read in 1 iter"),
        pytest.param(8, 2, [4, 0], 4, id="exact final match, 2 iters"),
        pytest.param(11, 2, [4, 8, 0], 4, id="exact final match, 3 iters"),
        pytest.param(19, 2, [4, 8, 12, 16, 0], 4, id="exact final match, 5 iters"),
        # pytest.param(1000, 2, range(4, 1000[4, 8, 12, 16, 0], 4, id="exact final match, 5 iters"),
    ],
)
def test_iterative_dataload_partials(
    num_rows: int,
    num_cols: int,
    next_index: int,
    max_records: int,
    create_random_csv: CsvGeneratorFunc,
):
    """Ensure that a csv containing MORE than MAX_RECORDS is loaded in multiple steps"""
    csv_path = create_random_csv(num_rows, num_cols)

    updated_index = 0
    for index in next_index:
        df_iterative, updated_index = load_data(
            csv_path, updated_index, num_rows=max_records
        )

        assert df_iterative.shape[0] > 0
        assert index == updated_index


def test_empty_file(create_random_csv: CsvGeneratorFunc):
    """Ensure that a empty CSV does not bomb out and returns an expected 
    null dataframe and 0 next index"""
    num_rows, num_cols = 0, 0
    csv_path = create_random_csv(num_rows, num_cols)

    updated_index = 0

    df, index = load_data(csv_path, updated_index, num_rows=100)

    assert df is None
    assert index == 0

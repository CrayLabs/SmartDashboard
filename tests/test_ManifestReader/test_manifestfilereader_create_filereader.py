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

from smartdashboard.utils.errors import ManifestError, VersionIncompatibilityError
from smartdashboard.utils.ManifestReader import ManifestFileReader, create_filereader


@pytest.mark.parametrize(
    "json_file, return_type",
    [
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json", ManifestFileReader
        ),
        pytest.param(
            "tests/utils/manifest_files/0.0.2_manifest.json",
            ManifestFileReader,
        ),
        pytest.param(
            "tests/utils/manifest_files/0.0.3_manifest.json",
            ManifestFileReader,
        ),
        pytest.param(
            "tests/utils/manifest_files/no_apps_manifest.json",
            ManifestFileReader,
        ),
        pytest.param("file_doesn't_exist.json", ManifestError),
        pytest.param("tests/utils/manifest_files/JSONDecodererror.json", ManifestError),
        pytest.param(
            "tests/utils/manifest_files/invalid_version.json",
            VersionIncompatibilityError,
        ),
    ],
)
def test_create_filereader(json_file, return_type):
    if return_type == ManifestError or return_type == VersionIncompatibilityError:
        with pytest.raises(return_type):
            create_filereader(json_file)
    else:
        manifest_reader = create_filereader(json_file)
        assert isinstance(manifest_reader, return_type)

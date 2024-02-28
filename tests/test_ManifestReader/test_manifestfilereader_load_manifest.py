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
from smartdashboard.utils.ManifestReader import (
    Manifest,
    ManifestFileReader,
    load_manifest,
)


@pytest.mark.parametrize(
    "json_file, manifest_type, reader_type",
    [
        pytest.param(
            "tests/utils/manifest_files/manifesttest.json", Manifest, ManifestFileReader
        ),
        pytest.param(
            "tests/utils/manifest_files/0.0.2_manifest.json",
            Manifest,
            ManifestFileReader,
        ),
        pytest.param(
            "tests/utils/manifest_files/no_apps_manifest.json",
            Manifest,
            ManifestFileReader,
        ),
        pytest.param("file_doesn't_exist.json", ManifestError, None),
        pytest.param(
            "tests/utils/manifest_files/JSONDecodererror.json", ManifestError, None
        ),
        pytest.param(
            "tests/utils/manifest_files/invalid_version.json",
            VersionIncompatibilityError,
            None,
        ),
    ],
)
def test_load_manifest_and_has_changed(json_file, manifest_type, reader_type):
    try:
        manifest, manifest_reader = load_manifest(json_file)
    except ManifestError:
        assert manifest_type == ManifestError
        return
    except VersionIncompatibilityError:
        assert manifest_type == VersionIncompatibilityError
        return

    assert type(manifest) == manifest_type
    assert type(manifest_reader) == reader_type
    assert manifest_reader._last_modified > 0.0
    assert manifest_reader.has_changed == False
    manifest_reader._last_modified = 0.0
    assert manifest_reader.has_changed == True

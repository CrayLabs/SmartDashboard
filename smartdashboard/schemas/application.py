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

import itertools
import typing as t

from smartdashboard.schemas.base import EntityWithNameTelemetryMetaDataErrOut
from smartdashboard.schemas.files import Files


class Application(EntityWithNameTelemetryMetaDataErrOut):
    path: str
    exe_args: t.List[str] = []
    run_settings: t.Dict[str, t.Any] = {}
    batch_settings: t.Dict[str, t.Any] = {}
    params: t.Dict[str, t.Any] = {}
    files: Files
    colocated_db: t.Dict[str, t.Any] = {}

    @property
    def loaded_entities(self) -> t.Mapping[str, t.Sequence[str]]:
        """Combine and format loaded entities

        DB Models and DB Scripts are combined so they can be displayed as
        "Loaded Entities" in the dashboard.

        :return: A list of formatted loaded entity dicts, or one formatted dict
        :rtype: Union[List[Dict[str, str]], Dict[str, List[Any]]]
        """
        models_ = self.colocated_db.get("models", [])
        models = (("DB Model", model) for model in models_)
        scripts_ = self.colocated_db.get("scripts", [])
        scripts = (("DB Script", script) for script in scripts_)

        combine = (item for item in itertools.chain(models, scripts))
        flatten = (
            (name, type_, info["backend"], info["device"])
            for type_, data in combine
            for name, info in data.items()
        )

        def take_idx(idx: int) -> t.Callable[[t.Any], t.Any]:
            return lambda xs: xs[idx]

        names, types, backends, devices = (
            map(take_idx(i), xss) for i, xss in enumerate(itertools.tee(flatten, 4))
        )

        return {
            "Name": tuple(names),
            "Type": tuple(types),
            "Backend": tuple(backends),
            "Device": tuple(devices),
        }

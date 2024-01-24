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

from smartdashboard.schemas.application import Application
from smartdashboard.schemas.ensemble import Ensemble
from smartdashboard.schemas.orchestrator import Orchestrator
from smartdashboard.schemas.run import Run
from smartdashboard.schemas.shard import Shard

application_1 = Application(
    name="app1",
    run_id="1",
    path="app/1/path",
    exe_args=["string"],
    batch_settings={
        "batch_cmd": "command",
        "batch_args": {"arg1": "string1", "arg2": None},
    },
    run_settings={
        "exe": "echo",
        "run_command": "srun",
        "run_args": {"arg1": "string1", "arg2": None},
    },
    params={"param": "param value"},
    files={
        "Symlink": ["file1", "file2"],
        "Configure": ["file3"],
        "Copy": ["file4", "file5"],
    },
    colocated_db={
        "settings": {
            "protocol": "TCP/IP",
            "port": 1111,
            "interface": "lo",
            "db_cpus": 1,
            "limit_app_cpus": "True",
            "debug": "False",
        },
        "scripts": [
            {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
            {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
        ],
        "models": [
            {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
            {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
        ],
    },
    telemetry_metadata={
        "status_dir": "tests/utils/status_files/model_0",
        "job_id": "111",
        "step_id": "111",
    },
    out_file="tests/utils/log_files/model_0.out",
    err_file="tests/utils/log_files/model_0.err",
)

application_2 = Application(
    name="app2",
    run_id="1",
    path="app/2/path",
    exe_args=["string1", "string2", "string3"],
    batch_settings={
        "batch_cmd": "command",
        "batch_args": {"arg1": "string1", "arg2": None},
    },
    run_settings={
        "exe": "echo",
        "run_command": "srun",
        "run_args": {"arg1": "string1", "arg2": None},
    },
    params={"string": ["Any"]},
    files={
        "Symlink": ["file1", "file2"],
        "Configure": ["file3"],
        "Copy": ["file4", "file5"],
    },
    colocated_db={
        "settings": {
            "protocol": "TCP/IP",
            "port": 1111,
            "interface": "lo",
            "db_cpus": 1,
            "limit_app_cpus": "True",
            "debug": "False",
        },
        "scripts": [
            {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
            {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
        ],
        "models": [
            {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
            {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
        ],
    },
    telemetry_metadata={
        "status_dir": "tests/utils/status_files/model_1",
        "job_id": "111",
        "step_id": "111",
    },
    out_file="tests/utils/log_files/model_1.out",
    err_file="tests/utils/log_files/model_1.err",
)

application_3 = Application(
    name="app3",
    run_id="2",
    path="app/3/path",
    exe_args=["string"],
    batch_settings={
        "batch_cmd": "command",
        "batch_args": {"arg1": "string1", "arg2": None},
    },
    run_settings={
        "exe": "echo",
        "run_command": "srun",
        "run_args": {"arg1": "string1", "arg2": None},
    },
    params={"string": "Any"},
    files={
        "Symlink": ["file1", "file2"],
        "Configure": ["file3"],
        "Copy": ["file4", "file5"],
    },
    colocated_db={
        "settings": {
            "protocol": "TCP/IP",
            "port": 1111,
            "interface": "lo",
            "db_cpus": 1,
            "limit_app_cpus": "True",
            "debug": "False",
        },
        "scripts": [],
        "models": [
            {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
            {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
        ],
    },
    telemetry_metadata={
        "status_dir": "tests/utils/status_files/model_3",
        "job_id": "111",
        "step_id": "111",
    },
    out_file="tests/utils/log_files/model_0.out",
    err_file="tests/utils/log_files/model_0.err",
)

application_4 = Application(
    name="app3",
    path="app/3/path",
    exe_args=["string"],
    batch_settings={
        "batch_cmd": "command",
        "batch_args": {"arg1": "string1", "arg2": None},
    },
    run_settings={
        "exe": "echo",
        "run_command": "srun",
        "run_args": {"arg1": "string1", "arg2": None},
    },
    params={"string": "Any"},
    files={
        "Symlink": ["file1", "file2"],
        "Configure": ["file3"],
        "Copy": ["file4", "file5"],
    },
    colocated_db={
        "settings": {
            "protocol": "TCP/IP",
            "port": 1111,
            "interface": "lo",
            "db_cpus": 1,
            "limit_app_cpus": "True",
            "debug": "False",
        },
        "scripts": [
            {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
            {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
        ],
        "models": [],
    },
    telemetry_metadata={
        "status_dir": "tests/utils/status_files/model_0",
        "job_id": "111",
        "step_id": "111",
    },
    out_file="tests/utils/log_files/model_0.out",
    err_file="tests/utils/log_files/model_0.err",
)

orchestrator_1 = Orchestrator(
    name="orchestrator_1",
    run_id="1",
    type="redis",
    interface=["lo", "lo2"],
    shards=[
        {
            "name": "shard 1",
            "hostname": "shard1_host",
            "port": "11111",
            "out_file": "tests/utils/log_files/model_1.out",
            "err_file": "tests/utils/log_files/model_1.err",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_3",
                "job_id": "111",
                "step_id": "111",
            },
            "client_file": "tests/utils/clients/client.csv",
            "client_count_file": "tests/utils/clients/client_counts.csv",
            "memory_file": "tests/utils/memory/memory.csv",
        },
        {
            "name": "shard 2",
            "hostname": "shard2_host",
            "port": "11111",
            "out_file": "tests/utils/log_files/model_0.out",
            "err_file": "tests/utils/log_files/model_0.err",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_1",
                "job_id": "111",
                "step_id": "111",
            },
            "client_file": "tests/utils/clients/client.csv",
            "client_count_file": "tests/utils/clients/client_counts.csv",
            "memory_file": "tests/utils/memory/memory.csv",
        },
    ],
)


orchestrator_2 = Orchestrator(
    name="orchestrator_2",
    run_id="2",
    type="redis",
    interface=["lo"],
    shards=[
        {
            "name": "orc 2 shard 1",
            "hostname": "shard1_host",
            "port": 22222,
            "out_file": "tests/utils/log_files/model_0.out",
            "err_file": "tests/utils/log_files/model_0.err",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_0",
                "job_id": "111",
                "step_id": "111",
            },
            "client_file": "tests/utils/clients/client.csv",
            "client_count_file": "tests/utils/clients/client_counts.csv",
            "memory_file": "tests/utils/memory/memory.csv",
        },
        {
            "name": "orc 2 shard 2",
            "hostname": "shard2_host",
            "port": 22222,
            "out_file": "tests/utils/log_files/model_1.out",
            "err_file": "tests/utils/log_files/model_1.err",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_1",
                "job_id": "111",
                "step_id": "111",
            },
            "client_file": "tests/utils/clients/client.csv",
            "client_count_file": "tests/utils/clients/client_counts.csv",
            "memory_file": "tests/utils/memory/memory.csv",
        },
    ],
)

orchestrator_3 = Orchestrator(
    name="orchestrator_3",
    run_id="2",
    type="redis",
    interface="lo",
    shards=[
        Shard(
            name="orc 3 shard 1",
            hostname="shard1_host",
            port="12345",
            out_file="tests/utils/log_files/orchestrator_0.out",
            err_file="tests/utils/log_files/orchestrator_0.err",
            conf_file="/path/to/conf_file",
            telemetry_metadata={
                "status_dir": "tests/utils/status_files/model_3",
                "job_id": "111",
                "step_id": "111",
            },
            client_file="tests/utils/clients/client.csv",
            client_count_file="tests/utils/clients/client_counts.csv",
            memory_file="tests/utils/memory/memory.csv",
        )
    ],
)

orchestrator_4 = Orchestrator(
    name="orchestrator_4",
    run_id="2",
    type="redis",
    interface="lo",
    shards=[
        {
            "name": "orc 3 shard 1",
            "hostname": "shard1_host",
            "port": "12345",
            "out_file": "tests/utils/log_files/orchestrator_0.out",
            "err_file": "tests/utils/log_files/orchestrator_0.err",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_0",
                "job_id": "111",
                "step_id": "111",
            },
            "client_file": "tests/utils/clients/client.csv",
            "client_count_file": "tests/utils/clients/client_counts.csv",
            "memory_file": "tests/utils/memory/memory.csv",
        }
    ],
)

no_shards_started = Orchestrator(
    name="orchestrator_2",
    type="redis",
    run_id="2",
    interface=["lo"],
    shards=[
        {
            "name": "orc 2 shard 1",
            "hostname": "shard1_host",
            "port": 22222,
            "out_file": "tests/utils/log_files/model_0.out",
            "err_file": "tests/utils/log_files/model_0.err",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_2",
                "job_id": "111",
                "step_id": "111",
            },
            "client_file": "tests/utils/clients/client.csv",
            "client_count_file": "tests/utils/clients/client_counts.csv",
            "memory_file": "tests/utils/memory/memory.csv",
        },
        {
            "name": "orc 2 shard 2",
            "hostname": "shard2_host",
            "port": 22222,
            "out_file": "tests/utils/log_files/model_1.out",
            "err_file": "tests/utils/log_files/model_1.err",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_2",
                "job_id": "111",
                "step_id": "111",
            },
            "client_file": "tests/utils/clients/client.csv",
            "client_count_file": "tests/utils/clients/client_counts.csv",
            "memory_file": "tests/utils/memory/memory.csv",
        },
    ],
)

mismatched_port_orchestrator = Orchestrator(
    name="orchestrator_1",
    type="redis",
    run_id="2",
    interface=["lo", "lo2"],
    shards=[
        {
            "name": "shard 1",
            "hostname": "shard1_host",
            "port": "11211",
            "out_file": "tests/utils/log_files/orchestrator_0.out",
            "err_file": "tests/utils/log_files/orchestrator_0.err",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_1",
                "job_id": "111",
                "step_id": "111",
            },
            "client_file": "tests/utils/clients/client.csv",
            "client_count_file": "tests/utils/clients/client_counts.csv",
            "memory_file": "tests/utils/memory/memory.csv",
        },
        {
            "name": "shard 2",
            "hostname": "shard2_host",
            "port": "11111",
            "out_file": "tests/utils/log_files/orchestrator_0.out",
            "err_file": "tests/utils/log_files/orchestrator_0.err",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_1us/dir",
                "job_id": "111",
                "step_id": "111",
            },
            "client_file": "tests/utils/clients/client.csv",
            "client_count_file": "tests/utils/clients/client_counts.csv",
            "memory_file": "tests/utils/memory/memory.csv",
        },
    ],
)

no_shards_orchestrator = Orchestrator(
    name="orchestrator_1",
    type="redis",
    run_id="2",
    interface=["lo", "lo2"],
    shards=[],
)

pending_shard = Shard(
    name="shard 2",
    hostname="shard2_host",
    port="11111",
    out_file="tests/utils/log_files/model_0.out",
    err_file="tests/utils/log_files/model_0.err",
    conf_file="/path/to/conf_file",
    telemetry_metadata={
        "status_dir": "tests/utils/status_files/model_2",
        "job_id": "111",
        "step_id": "111",
    },
    client_file="tests/utils/clients/client.csv",
    client_count_file="tests/utils/clients/client_counts.csv",
    memory_file="tests/utils/memory/memory.csv",
)

no_return_code_shard = Shard(
    name="shard 2",
    hostname="shard2_host",
    port="11111",
    out_file="tests/utils/log_files/model_0.out",
    err_file="tests/utils/log_files/model_0.err",
    conf_file="/path/to/conf_file",
    telemetry_metadata={
        "status_dir": "tests/utils/status_files/model_4",
        "job_id": "111",
        "step_id": "111",
    },
    client_file="tests/utils/clients/client.csv",
    client_count_file="tests/utils/clients/client_counts.csv",
    memory_file="tests/utils/memory/memory.csv",
)

malformed_status_dir_shard = Shard(
    name="shard 2",
    hostname="shard2_host",
    port="11111",
    out_file="tests/utils/log_files/model_0.out",
    err_file="tests/utils/log_files/model_0.err",
    conf_file="/path/to/conf_file",
    telemetry_metadata={
        "statdir": "tests/utils/status_files/model_3",
        "job_id": "111",
        "step_id": "111",
    },
    client_file="tests/utils/clients/client.csv",
    client_count_file="tests/utils/clients/client_counts.csv",
    memory_file="tests/utils/memory/memory.csv",
)

JSONDecoderError_status_shard = Shard(
    name="shard 2",
    hostname="shard2_host",
    port="11111",
    out_file="tests/utils/log_files/model_0.out",
    err_file="tests/utils/log_files/model_0.err",
    conf_file="/path/to/conf_file",
    telemetry_metadata={
        "status_dir": "tests/utils/manifest_files/JSONDecodererror.json",
        "job_id": "111",
        "step_id": "111",
    },
    client_file="tests/utils/clients/client.csv",
    client_count_file="tests/utils/clients/client_counts.csv",
    memory_file="tests/utils/memory/memory.csv",
)

ensemble_1 = Ensemble(
    name="ensemble_1",
    run_id="1",
    perm_strat="string0",
    batch_settings={"string": "Any0"},
    params={"string": ["Any1", "Any3"]},
    models=[
        {
            "name": "ensemble_1_member_1",
            "path": "string",
            "exe_args": ["string"],
            "batch_settings": {
                "batch_cmd": "command",
                "batch_args": {"arg1": "string1", "arg2": None},
            },
            "run_settings": {
                "exe": "echo",
                "run_command": "srun",
                "run_args": {"arg1": "string1", "arg2": None},
            },
            "params": {"string": "Any"},
            "files": {
                "Symlink": ["file1", "file2"],
                "Configure": ["file3"],
                "Copy": ["file4", "file5"],
            },
            "colocated_db": {
                "settings": {
                    "protocol": "TCP/IP",
                    "port": 1111,
                    "interface": "lo",
                    "db_cpus": 1,
                    "limit_app_cpus": "True",
                    "debug": "False",
                },
                "scripts": [
                    {
                        "script1": {
                            "backend": "script1_torch",
                            "device": "script1_cpu",
                        }
                    },
                    {
                        "script2": {
                            "backend": "script2_torch",
                            "device": "script2_gpu",
                        }
                    },
                ],
                "models": [
                    {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
                    {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
                ],
            },
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_0",
                "job_id": "111",
                "step_id": "111",
            },
            "out_file": "tests/utils/log_files/model_0.out",
            "err_file": "tests/utils/log_files/model_0.err",
        }
    ],
)


ensemble_2 = Ensemble(
    name="ensemble_2",
    run_id="1",
    perm_strat="all-perm",
    batch_settings={"string": "Any1"},
    params={"string": ["Any1", "Any2", "Any3"]},
    models=[],
)

ensemble_3 = Ensemble(
    name="ensemble_3",
    run_id="2",
    perm_strat="string2",
    batch_settings={"string": "Any1"},
    params={"string": ["Any1", "Any2", "Any3"]},
    models=[
        {
            "name": "ensemble_3_member_1",
            "path": "member 1 path",
            "exe_args": ["string"],
            "batch_settings": {
                "batch_cmd": "command",
                "batch_args": {"arg1": "string1", "arg2": None},
            },
            "run_settings": {
                "exe": "echo",
                "run_command": "srun",
                "run_args": {"arg1": "string1", "arg2": None},
            },
            "params": {"string": "Any"},
            "files": {
                "Symlink": ["file1", "file2"],
                "Configure": ["file3"],
                "Copy": ["file4", "file5"],
            },
            "colocated_db": {
                "settings": {
                    "protocol": "TCP/IP",
                    "port": 1111,
                    "interface": "lo",
                    "db_cpus": 1,
                    "limit_app_cpus": "True",
                    "debug": "False",
                },
                "scripts": [
                    {
                        "script1": {
                            "backend": "script1_torch",
                            "device": "script1_cpu",
                        }
                    },
                    {
                        "script2": {
                            "backend": "script2_torch",
                            "device": "script2_gpu",
                        }
                    },
                ],
                "models": [
                    {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
                    {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
                ],
            },
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_3",
                "job_id": "111",
                "step_id": "111",
            },
            "out_file": "tests/utils/log_files/model_0.out",
            "err_file": "tests/utils/log_files/model_0.err",
        },
        {
            "name": "ensemble_3_member_2",
            "path": "member 2 path",
            "exe_args": ["string"],
            "batch_settings": {
                "batch_cmd": "command",
                "batch_args": {"arg1": "string1"},
            },
            "run_settings": {
                "exe": "echo",
                "run_command": "srun",
                "run_args": {"arg1": "string1", "arg2": None},
            },
            "params": {"string": "Any"},
            "files": {
                "Symlink": ["file1", "file2"],
                "Configure": ["file3"],
                "Copy": ["file4", "file5"],
            },
            "colocated_db": {
                "settings": {
                    "protocol": "TCP/IP",
                    "port": 1111,
                    "interface": "lo",
                    "db_cpus": 1,
                    "limit_app_cpus": "True",
                    "debug": "False",
                },
                "scripts": [
                    {
                        "script1": {
                            "backend": "script1_torch",
                            "device": "script1_cpu",
                        }
                    },
                    {
                        "script2": {
                            "backend": "script2_torch",
                            "device": "script2_gpu",
                        }
                    },
                ],
                "models": [
                    {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
                    {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
                ],
            },
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_1",
                "job_id": "111",
                "step_id": "111",
            },
            "out_file": "tests/utils/log_files/model_1.out",
            "err_file": "tests/utils/log_files/model_1.err",
        },
    ],
)


ensemble_4 = Ensemble(
    name="ensemble_3",
    perm_strat="string2",
    run_id="2",
    batch_settings={"string": "Any1"},
    params={"string": ["Any1", "Any2", "Any3"]},
    models=[
        {
            "name": "ensemble_3_member_1",
            "path": "member 1 path",
            "exe_args": ["string"],
            "batch_settings": {
                "batch_cmd": "command",
                "batch_args": {"arg1": "string1", "arg2": None},
            },
            "run_settings": {
                "exe": "echo",
                "run_command": "srun",
                "run_args": {"arg1": "string1", "arg2": None},
            },
            "params": {"string": "Any"},
            "files": {
                "Symlink": ["file1", "file2"],
                "Configure": ["file3"],
                "Copy": ["file4", "file5"],
            },
            "colocated_db": {
                "settings": {
                    "protocol": "TCP/IP",
                    "port": 1111,
                    "interface": "lo",
                    "db_cpus": 1,
                    "limit_app_cpus": "True",
                    "debug": "False",
                },
                "scripts": [
                    {
                        "script1": {
                            "backend": "script1_torch",
                            "device": "script1_cpu",
                        }
                    },
                    {
                        "script2": {
                            "backend": "script2_torch",
                            "device": "script2_gpu",
                        }
                    },
                ],
                "models": [
                    {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
                    {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
                ],
            },
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_1",
                "job_id": "111",
                "step_id": "111",
            },
            "out_file": "tests/utils/log_files/model_0.out",
            "err_file": "tests/utils/log_files/model_0.err",
        },
        {
            "name": "ensemble_3_member_2",
            "path": "member 2 path",
            "exe_args": ["string"],
            "batch_settings": {
                "batch_cmd": "command",
                "batch_args": {"arg1": "string1"},
            },
            "run_settings": {
                "exe": "echo",
                "run_command": "srun",
                "run_args": {"arg1": "string1", "arg2": None},
            },
            "params": {"string": "Any"},
            "files": {
                "Symlink": ["file1", "file2"],
                "Configure": ["file3"],
                "Copy": ["file4", "file5"],
            },
            "colocated_db": {
                "settings": {
                    "protocol": "TCP/IP",
                    "port": 1111,
                    "interface": "lo",
                    "db_cpus": 1,
                    "limit_app_cpus": "True",
                    "debug": "False",
                },
                "scripts": [
                    {
                        "script1": {
                            "backend": "script1_torch",
                            "device": "script1_cpu",
                        }
                    },
                    {
                        "script2": {
                            "backend": "script2_torch",
                            "device": "script2_gpu",
                        }
                    },
                ],
                "models": [
                    {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
                    {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
                ],
            },
            "telemetry_metadata": {
                "status_dir": "tests/utils/status_files/model_1",
                "job_id": "111",
                "step_id": "111",
            },
            "out_file": "tests/utils/log_files/model_1.out",
            "err_file": "tests/utils/log_files/model_1.err",
        },
    ],
)

no_db_scripts_or_models = Application(
    name="no scripts or models",
    path="member 2 path",
    exe_args=["string"],
    batch_settings={"batch_cmd": "command", "batch_args": {"arg1": "string1"}},
    run_settings={
        "exe": "echo",
        "run_command": "srun",
        "run_args": {"arg1": "string1", "arg2": None},
    },
    params={"string": "Any"},
    files={
        "Symlink": ["file1", "file2"],
        "Configure": ["file3"],
        "Copy": ["file4", "file5"],
    },
    colocated_db={
        "settings": {
            "protocol": "TCP/IP",
            "port": 1111,
            "interface": "lo",
            "db_cpus": 1,
            "limit_app_cpus": "True",
            "debug": "False",
        },
        "scripts": [],
        "models": [],
    },
    telemetry_metadata={
        "status_dir": "tests/utils/status_files/model_1",
        "job_id": "111",
        "step_id": "111",
    },
    out_file="tests/utils/log_files/model_1.out",
    err_file="tests/utils/log_files/model_1.err",
)

model0_out_logs = """SmartRedis Library@16-04-21:WARNING: Environment variable SR_LOG_FILE is not set. Defaulting to stdout
SmartRedis Library@16-04-21:WARNING: Environment variable SR_LOG_LEVEL is not set. Defaulting to INFO
Freq (hz) = 0.1
Sleep time = 10.0
Number of messages = 10
"""

model0_err_logs = """Traceback (most recent call last):
  File "/lus/cls01029/mellis/cray_labs/SmartSim/tests/test_configs/bad.py", line 42, in <module>
    divide_by_zero(args.time)
  File "/lus/cls01029/mellis/cray_labs/SmartSim/tests/test_configs/bad.py", line 34, in divide_by_zero
    print(1 / 0)
ZeroDivisionError: division by zero"""

model1_out_logs = """SmartRedis Library@16-04-21:WARNING: Environment variable SR_LOG_FILE is not set. Defaulting to stdout
SmartRedis Library@16-04-21:WARNING: Environment variable SR_LOG_LEVEL is not set. Defaulting to INFO
Freq (hz) = 1.0
Sleep time = 1.0
Number of messages = 100"""

model1_err_logs = """Traceback (most recent call last):
  File "/lus/cls01029/alyssacote/cray_labs/SmartSim/tests/test_configs/bad.py", line 42, in <module>
    divide_by_zero(args.time)
  File "/lus/cls01029/alyssacote/cray_labs/SmartSim/tests/test_configs/bad.py", line 34, in divide_by_zero
    print(1 / 0)
ZeroDivisionError: division by zero"""

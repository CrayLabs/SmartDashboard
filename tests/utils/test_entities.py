application_1 = {
    "name": "app1",
    "run_id": 1,
    "path": "app/1/path",
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
    "params": {"param": "param value"},
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
            {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
            {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
        ],
        "models": [
            {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
            {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
        ],
    },
    "telemetry_metadata": {
        "status_dir": "/path/to/status dir",
        "job_id": "111",
        "step_id": 111,
    },
    "out_file": "test_dashboard/log_files/model_0.out",
    "err_file": "test_dashboard/log_files/model_0.err",
}

application_2 = {
    "name": "app2",
    "run_id": 1,
    "path": "app/2/path",
    "exe_args": ["string1", "string2", "string3"],
    "batch_settings": {
        "batch_cmd": "command",
        "batch_args": {"arg1": "string1", "arg2": None},
    },
    "run_settings": {
        "exe": "echo",
        "run_command": "srun",
        "run_args": {"arg1": "string1", "arg2": None},
    },
    "params": {"string": ["Any"]},
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
            {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
            {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
        ],
        "models": [
            {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
            {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
        ],
    },
    "telemetry_metadata": {
        "status_dir": "/path/to/status dir",
        "job_id": "111",
        "step_id": 111,
    },
    "out_file": "test_dashboard/log_files/model_1.out",
    "err_file": "test_dashboard/log_files/model_1.err",
}

application_3 = {
    "name": "app3",
    "run_id": 2,
    "path": "app/3/path",
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
        "scripts": [],
        "models": [
            {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
            {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
        ],
    },
    "telemetry_metadata": {
        "status_dir": "/path/to/status dir",
        "job_id": "111",
        "step_id": 111,
    },
    "out_file": "test_dashboard/log_files/model_0.out",
    "err_file": "test_dashboard/log_files/model_0.err",
}
application_4 = {
    "name": "app3",
    "path": "app/3/path",
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
            {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
            {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
        ],
        "models": [],
    },
    "telemetry_metadata": {
        "status_dir": "/path/to/status dir",
        "job_id": "111",
        "step_id": 111,
    },
    "out_file": "test_dashboard/log_files/model_0.out",
    "err_file": "test_dashboard/log_files/model_0.err",
}

orchestrator_1 = {
    "name": "orchestrator_1",
    "run_id": 1,
    "type": "redis",
    "interface": ["lo", "lo2"],
    "shards": [
        {
            "name": "shard 1",
            "host": "shard1_host",
            "port": "11111",
            "out_file": "/path/to/shard/output/logs",
            "err_file": "/path/to/shard/error/logs",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "/path/to/status/dir",
                "job_id": "111",
                "step_id": 111,
            },
        },
        {
            "name": "shard 2",
            "host": "shard2_host",
            "port": "11111",
            "out_file": "/path/to/shard/output/logs",
            "err_file": "/path/to/shard/error/logs",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "/path/to/status/dir",
                "job_id": "111",
                "step_id": 111,
            },
        },
    ],
}

orchestrator_2 = {
    "name": "orchestrator_2",
    "run_id": 2,
    "type": "redis",
    "interface": ["lo"],
    "shards": [
        {
            "name": "orc 2 shard 1",
            "host": "shard1_host",
            "port": 22222,
            "out_file": "/path/to/shard/output/logs",
            "err_file": "/path/to/shard/error/logs",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "/path/to/status/dir",
                "job_id": "111",
                "step_id": 111,
            },
        },
        {
            "name": "orc 2 shard 2",
            "host": "shard2_host",
            "port": 22222,
            "out_file": "/path/to/shard/output/logs",
            "err_file": "/path/to/shard/error/logs",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "/path/to/status/dir",
                "job_id": "111",
                "step_id": 111,
            },
        },
    ],
}

orchestrator_3 = {
    "name": "orchestrator_3",
    "run_id": 2,
    "type": "redis",
    "interface": "lo",
    "shards": [
        {
            "name": "orc 3 shard 1",
            "host": "shard1_host",
            "port": "12345",
            "out_file": "/path/to/shard/output/logs",
            "err_file": "/path/to/shard/error/logs",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "/path/to/status/dir",
                "job_id": "111",
                "step_id": 111,
            },
        }
    ],
}

mismatched_port_orchestrator = {
    "name": "orchestrator_1",
    "type": "redis",
    "interface": ["lo", "lo2"],
    "shards": [
        {
            "name": "shard 1",
            "host": "shard1_host",
            "port": "11211",
            "out_file": "/path/to/shard/output/logs",
            "err_file": "/path/to/shard/error/logs",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "/path/to/status/dir",
                "job_id": "111",
                "step_id": 111,
            },
        },
        {
            "name": "shard 2",
            "host": "shard2_host",
            "port": "11111",
            "out_file": "/path/to/shard/output/logs",
            "err_file": "/path/to/shard/error/logs",
            "conf_file": "/path/to/conf_file",
            "telemetry_metadata": {
                "status_dir": "/path/to/status/dir",
                "job_id": "111",
                "step_id": 111,
            },
        },
    ],
}

no_shards_orchestrator = {
    "name": "orchestrator_1",
    "type": "redis",
    "interface": ["lo", "lo2"],
    "shards": [],
}

ensemble_1 = {
    "name": "ensemble_1",
    "run_id": 1,
    "perm_strat": "string0",
    "batch_settings": {"string": "Any0"},
    "params": {"string": ["Any1", "Any3"]},
    "models": [
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
                    {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
                    {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
                ],
                "models": [
                    {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
                    {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
                ],
            },
            "telemetry_metadata": {
                "status_dir": "/path/to/status dir",
                "job_id": "111",
                "step_id": 111,
            },
            "out_file": "test_dashboard/log_files/model_0.out",
            "err_file": "test_dashboard/log_files/model_0.err",
        }
    ],
}


ensemble_1_member_1 = {
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
            {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
            {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
        ],
        "models": [
            {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
            {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
        ],
    },
    "telemetry_metadata": {
        "status_dir": "/path/to/status dir",
        "job_id": "111",
        "step_id": 111,
    },
    "out_file": "test_dashboard/log_files/model_0.out",
    "err_file": "test_dashboard/log_files/model_0.err",
}

ensemble_2 = {
    "name": "ensemble_2",
    "perm_strat": "all-perm",
    "batch_settings": {"string": "Any1"},
    "params": {"string": ["Any1", "Any2", "Any3"]},
    "models": [],
}

ensemble_3 = {
    "name": "ensemble_3",
    "run_id": 2,
    "perm_strat": "string2",
    "batch_settings": {"string": "Any1"},
    "params": {"string": ["Any1", "Any2", "Any3"]},
    "models": [
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
                    {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
                    {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
                ],
                "models": [
                    {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
                    {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
                ],
            },
            "telemetry_metadata": {
                "status_dir": "/path/to/status dir",
                "job_id": "111",
                "step_id": 111,
            },
            "out_file": "test_dashboard/log_files/model_0.out",
            "err_file": "test_dashboard/log_files/model_0.err",
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
                    {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
                    {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
                ],
                "models": [
                    {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
                    {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
                ],
            },
            "telemetry_metadata": {
                "status_dir": "/path/to/status dir",
                "job_id": "111",
                "step_id": 111,
            },
            "out_file": "test_dashboard/log_files/model_1.out",
            "err_file": "test_dashboard/log_files/model_1.err",
        },
    ],
}

ensemble_3_member_1 = {
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
            {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
            {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
        ],
        "models": [
            {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
            {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
        ],
    },
    "telemetry_metadata": {
        "status_dir": "/path/to/status dir",
        "job_id": "111",
        "step_id": 111,
    },
    "out_file": "test_dashboard/log_files/model_0.out",
    "err_file": "test_dashboard/log_files/model_0.err",
}

ensemble_3_member_2 = {
    "name": "ensemble_3_member_2",
    "path": "member 2 path",
    "exe_args": ["string"],
    "batch_settings": {"batch_cmd": "command", "batch_args": {"arg1": "string1"}},
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
            {"script1": {"backend": "script1_torch", "device": "script1_cpu"}},
            {"script2": {"backend": "script2_torch", "device": "script2_gpu"}},
        ],
        "models": [
            {"model1": {"backend": "model1_tf", "device": "model1_cpu"}},
            {"model2": {"backend": "model2_tf", "device": "model2_cpu"}},
        ],
    },
    "telemetry_metadata": {
        "status_dir": "/path/to/status dir",
        "job_id": "111",
        "step_id": 111,
    },
    "out_file": "test_dashboard/log_files/model_1.out",
    "err_file": "test_dashboard/log_files/model_1.err",
}


no_db_scripts_or_models = {
    "name": "no scripts or models",
    "path": "member 2 path",
    "exe_args": ["string"],
    "batch_settings": {"batch_cmd": "command", "batch_args": {"arg1": "string1"}},
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
        "scripts": [],
        "models": [],
    },
    "telemetry_metadata": {
        "status_dir": "/path/to/status dir",
        "job_id": "111",
        "step_id": 111,
    },
    "out_file": "test_dashboard/log_files/model_1.out",
    "err_file": "test_dashboard/log_files/model_1.err",
}
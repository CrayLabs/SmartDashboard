# SmartDashboard

SmartDashboard is an add-on to SmartSim that provides a dashboard to help users understand and monitor their SmartSim experiments in a visual way. Configuration, status, and logs are available for all launched entities within an experiment for easy inspection, along with memory and client data per shard for launched orchestrators.

A ``Telemetry Monitor`` is a background process that is launched alongside the experiment.
It is responsible for generating the data displayed by SmartDashboard. The ``Telemetry Monitor`` can be disabled globally by
adding ``export SMARTSIM_FLAG_TELEMETRY=0`` as an environment variable. When disabled, SmartDashboard
will not display entity status data. To re-enable, set the ``SMARTSIM_FLAG_TELEMETRY`` environment variable to ``1``
with ``export SMARTSIM_FLAG_TELEMETRY=1``. For workflows involving multiple experiments, SmartSim provides the attributes
``Experiment.telemetry.enable`` and ``Experiment.telemetry.disable`` to manage the enabling or disabling of telemetry on a per-experiment basis.

`Orchestrator` memory and client data can be collected by enabling database telemetry. To do so, add ``Orchestrator.telemetry.enable``
after creating an `Orchestrator` within the driver script. Database telemetry is enabled per `Orchestrator`, so if there are multiple
`Orchestrators` launched, they will each need to be enabled separately in the driver script.

```python
# enabling telemetry example

from smartsim import Experiment

exp = Experiment("experiment", launcher="auto")
exp.telemetry.enable()

db = exp.create_database(db_nodes=3)
db.telemetry.enable()

exp.start(db, block=True)
exp.stop(db)
```

Experiment metadata is stored in the ``.smartsim`` directory, a hidden folder used by the internal api and accessed by the dashboard.
This folder can be found within the created experiment directory.
Deletion of the experiment folder will remove all associated metadata.

## Installation

It's important to note that SmartDashboard only works while using SmartSim, so SmartSim will need to be installed as well.
SmartSim installation docs can be found [here](https://www.craylabs.org/docs/installation_instructions/basic.html).

### User Install

Run `pip install smartdashboard` to install SmartDashboard without cloning the repository.

### Developer Install

Clone the `SmartDashboard` repository at https://github.com/CrayLabs/SmartDashboard.git

Once cloned, `cd` into the repository and run:

```pip install -e .```

## Running SmartDashboard

After launching a SmartSim experiment, the dashboard can be launched using SmartSim's CLI.
  
```smart dashboard --port <port number> --directory <experiment directory path>```
  
The port can optionally be specified, otherwise the dashboard port will default to `8501`.
The directory must be specified and should be a relative or absolute path to the created experiment directory.

Example workflow:

```bash
# directory before running experiment
├── hello_world.py
```

```python
# hello_world.py
from smartsim import Experiment

exp = Experiment("hello_world_exp", launcher="auto")
exp.telemetry.enable()
run = exp.create_run_settings(exe="echo", exe_args="Hello World!")
run.set_tasks(60)
run.set_tasks_per_node(20)

model = exp.create_model("hello_world", run)
exp.start(model, block=True, summary=True)
```

```bash
# in interactive terminal
python hello_world.py
```

```bash
# directory after running experiment
├── hello_world.py
└── hello_world_exp
```

By default, `hello_world_exp` is created in the directory of the driver script.

```bash
# in a different interactive terminal
smart dashboard --port 8888 --directory hello_world_exp
```

The dashboard will automatically open in a browser at port 8888 when `smart dashboard ...` 
is invoked locally.

> If the dashboard is executed remotely, establishing port-forwarding to the
> remote machine will be necessary. This may be accomplished with ssh as follows:
>
> ```bash
> # using ssh to establish port forwarding 
> ssh -L [local-addr]:<local-port>:<remote-addr>:<remote-port> <user-id>@<remote-addr>
> # example forwarding the remote port 8888 to localhost:8000
> ssh -L localhost:8000:super1.my.domain.net:8888 smartdash@super1.my.domain.net
> ```
>
> After establishing the port-forwarding, a local browser can be pointed at the appropriate 
> URL, such as `http://localhost:8000` for the example above.

The dashboard is also persistent, meaning that a user can still launch and use the dashboard even after the experiment has completed.

## Using SmartDashboard

Once the dashboard is launched, a browser will open to `http://localhost:<port>`. SmartDashboard currently has two tabs on the left hand side.
  
`Experiment Overview:` This tab is where configuration information, statuses, and logs are located for each launched entity of the experiment. The `Experiment` section displays configuration information for the overall experiment and its logs. In the `Applications` section, also known as SmartSim `Models`, select a launched application to see its status, what it was configured with, and its logs. The `Orchestrators` section also provides configuration and status information, as well as logs per shard for a selected orchestrator. Finally, in the `Ensembles` section, select an ensemble to see its status and configuration. Then select any of its members to see its status, configuration, and logs.
  
`Database Telemetry:` This tab provides additional details about `Orchestrators`.
The `Orchestrator Summary` section shows configuration and status information of the selected. The `Memory`
section provides memory usage data per shard within the `Orchestrator`. The `Clients`
section displays client data per shard within the `Orchestrator`.  

`Help:` This tab links to SmartSim documentation and provides a SmartSim contact for support.

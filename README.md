# Interoperability IRIS Python Training

This training teaches InterSystems IRIS interoperability with Embedded Python and
`iris-pex-embedded-python` version 4.

The v4 best practice is to author the production in Python with the
`Production` API. The production topology is no longer hand-written as nested
IRIS production dictionaries. Python classes, component instances, settings,
ports, and connections are declared together in `src/settings.py`.

Reference documentation:

- https://grongierisc.github.io/interoperability-embedded-python/
- https://grongierisc.github.io/interoperability-embedded-python/changelog/
- https://grongierisc.github.io/interoperability-embedded-python/production-graph-roadmap/

As of June 2, 2026, v4 is marked as unreleased in the changelog. This template
uses the v4 beta package pinned in `requirements.txt`.

## Table Of Contents

- [1. Framework](#1-framework)
- [2. Training Scenario](#2-training-scenario)
- [3. Prerequisites](#3-prerequisites)
- [4. Setup](#4-setup)
- [5. v4 Production API Basics](#5-v4-production-api-basics)
- [6. Warm Up: Hello World Operation](#6-warm-up-hello-world-operation)
- [7. Part 1: CSV To Text File Pipeline](#7-part-1-csv-to-text-file-pipeline)
- [8. Part 2: Add A Process And PostgreSQL Operation](#8-part-2-add-a-process-and-postgresql-operation)
- [9. Useful v4 Commands](#9-useful-v4-commands)

## 1. Framework

This is the IRIS interoperability framework.

![FrameworkFull](https://raw.githubusercontent.com/thewophile-beep/formation-template/master/misc/img/FrameworkFull.png)

A production is a set of runtime components:

- Business Services receive data from external systems or scheduled work.
- Business Processes orchestrate and transform messages.
- Business Operations execute technical work, such as writing files or calling
  external systems.
- Messages are the contracts exchanged between components.
- Adapters connect components to external protocols or scheduled polling.

## 2. Training Scenario

In this training, we will read lines from a CSV file and send each row through
an IRIS interoperability production.

First, the production writes rows to a text file.

Then, we add a business process that routes each row to both:

- a text-file operation
- a PostgreSQL operation

The adapted framework looks like this:

![FrameworkAdapted](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/Main_Diagram.drawio.png)

## 3. Prerequisites

Install:

- VS Code: https://code.visualstudio.com/
- InterSystems VS Code extensions: https://intersystems-community.github.io/vscode-objectscript/installation/
- Docker: https://docs.docker.com/get-docker/
- The Docker extension for VS Code

The PostgreSQL and Flask Python dependencies are installed from
`requirements.txt`.

## 4. Setup

### 4.1. Start The Containers

Start IRIS and PostgreSQL:

```bash
$ docker-compose up -d
```

The project root is mounted in the IRIS container as `/irisdev/app`.

Open a shell inside the IRIS container:

```bash
$ docker-compose exec iris bash
```

The container sets `PYTHONPATH=/irisdev/app/src`. This matters when the `iop`
CLI deserializes Python messages returned by a component. If you use an older
container that was created before this setting was added, either recreate it or
run this once in the shell:

```bash
% export PYTHONPATH=/irisdev/app/src:$PYTHONPATH
```

In this README:

- commands prefixed with `$` run on your host terminal
- commands prefixed with `%` run inside the IRIS container

### 4.2. Create A Local Python Virtual Environment

The local virtual environment is useful for editing, autocomplete, and running
small Python checks from the host.

```bash
$ python3 -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

If activation is blocked:

```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force; .venv\Scripts\Activate.ps1
```

## 5. v4 Production API Basics

Version 4 adds a Python DSL for productions. A `Production` object is the
source of truth for Python-authored topology.

The core pattern is:

```python
from iop import Production

prod = Production("MyIRIS.Production", testing_enabled=True)

service = prod.service("Instance.Of.Service", ServiceClass)
process = prod.process("Instance.Of.Process", ProcessClass)
operation = prod.operation("Instance.Of.Operation", OperationClass)

prod.connect(service.target, process)
prod.connect(process.target, operation)

PRODUCTIONS = [prod]
```

Important v4 habits:

- Use `Production(...)` instead of hand-writing nested `PRODUCTIONS`
  dictionaries.
- Use `prod.service`, `prod.process`, and `prod.operation` to declare
  production items.
- Use `target()` on component classes to declare outbound ports.
- Use `prod.connect(source_port, target_component)` to route one port to one
  target.
- Use `prod.connect_add(source_port, target_component)` only when one port must
  fan out to several targets.
- Keep `PRODUCTIONS = [prod]` in `settings.py`. During migration, v4
  automatically registers Python component classes referenced by the production.
- Do not register simple `Message` dataclasses in `CLASSES`. They are serialized
  by IoP and only need schema registration when used for DTL support.

Legacy `CLASSES` still exists for special cases, but it is no longer the main
way to teach Python-authored productions.

## 6. Warm Up: Hello World Operation

### 6.1. Create The Package

Create the package:

```bash
$ mkdir -p src/hello_world
$ touch src/hello_world/__init__.py
```

Create `src/hello_world/bo.py`:

```python
from iop import BusinessOperation


class MyBo(BusinessOperation):
    def on_message(self, request):
        self.log_info("Hello World")
```

`on_message` is the generic handler. It receives any message that does not have
a more specific typed handler.

### 6.2. Create The Production

Create `src/settings.py`:

```python
from hello_world.bo import MyBo
from iop import Production


prod = Production("MyIRIS.Production", testing_enabled=True)
my_bo = prod.operation("Instance.Of.MyBo", MyBo)

PRODUCTIONS = [prod]
```

This declares:

- one IRIS production named `MyIRIS.Production`
- one business operation item named `Instance.Of.MyBo`
- one Python component class, registered automatically during migration

### 6.3. Migrate, Start, And Test

Inside the IRIS container:

```bash
% iop --migrate /irisdev/app/src/settings.py --dry-run
% iop --migrate /irisdev/app/src/settings.py
% iop --start MyIRIS.Production --detach
% iop --test Instance.Of.MyBo
% iop --log
```

Press `Ctrl+C` to exit the log stream.

The `--dry-run` step is a v4 best practice. It prints and validates the
migration plan before writing to IRIS.

### 6.4. Add A Message

Create `src/hello_world/msg.py`:

```python
from dataclasses import dataclass

from iop import Message


@dataclass
class MyMsg(Message):
    value: str = ""
```

Messages used only for Python serialization do not need to be added to
`CLASSES`.

### 6.5. Add A Typed Handler

Replace `src/hello_world/bo.py` with:

```python
from hello_world.msg import MyMsg
from iop import BusinessOperation


class MyBo(BusinessOperation):
    def on_message(self, request):
        response = MyMsg()
        response.value = "Hello World"
        return response

    def on_my_msg(self, request: MyMsg):
        response = MyMsg()
        response.value = f"Hello World {request.value}"
        return response
```

In v4, typed dispatch is based on the single typed parameter. The method name is
for readability, but the important part is `request: MyMsg`.

Reload and test:

```bash
% iop --migrate /irisdev/app/src/settings.py
% iop --update
% export PYTHONPATH=/irisdev/app/src:$PYTHONPATH
% iop --test Instance.Of.MyBo
% iop --test Instance.Of.MyBo --classname hello_world.msg.MyMsg --body '{"value": "of IRIS"}'
```

Expected typed response:

```text
hello_world.msg.MyMsg : {"value": "Hello World of IRIS"}
```

## 7. Part 1: CSV To Text File Pipeline

We will now read `misc/formation.csv` and write each row to
`data/formation.txt`.

![Pipeline](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/Main_Diagram_part1.drawio.png)

Create the package:

```bash
$ mkdir -p src/training
$ touch src/training/__init__.py
```

### 7.1. Message

Create `src/training/msg.py`:

```python
from dataclasses import dataclass

from iop import Message


@dataclass
class FormationRequest(Message):
    id: int = 0
    nom: str = ""
    salle: str = ""
```

The CSV format is:

```csv
id;nom;salle
1;Formation IRIS;Paris
2;Formation IRIS;Lyon
```

### 7.2. Text File Operation

Create `src/training/bo.py`:

```python
import os
from typing import Annotated

from iop import BusinessOperation, Category, controls, setting
from training.msg import FormationRequest


class SaveInTxtBo(BusinessOperation):
    filename: Annotated[str, setting(
        "formation.txt",
        category=Category.BASIC,
        description="Output file name.",
    )]
    path: Annotated[str, setting(
        "/irisdev/app/data/",
        category=Category.BASIC,
        description="Output directory.",
        control=controls.directory(),
    )]

    def on_init(self):
        os.makedirs(self.path, exist_ok=True)

    def on_formation_request(self, request: FormationRequest):
        output_file = os.path.join(self.path, self.filename)
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"{request.id};{request.nom};{request.salle}\n")

        self.log_info(f"FormationRequest {request.id} saved in {output_file}")
```

The `setting(...)` metadata exposes component settings in the IRIS production
portal and gives them Python defaults.

### 7.3. Update The Production

Replace `src/settings.py` with:

```python
from hello_world.bo import MyBo
from iop import Production
from training.bo import SaveInTxtBo


prod = Production("MyIRIS.Production", testing_enabled=True)

my_bo = prod.operation("Instance.Of.MyBo", MyBo)
save_txt = prod.operation("Instance.Of.SaveInTxtBo", SaveInTxtBo)

PRODUCTIONS = [prod]
```

Migrate and update the running production:

```bash
% iop --migrate /irisdev/app/src/settings.py --dry-run
% iop --migrate /irisdev/app/src/settings.py
% iop --update
```

Test the operation:

```bash
% iop --test Instance.Of.SaveInTxtBo --classname training.msg.FormationRequest --body '{"id": 1, "nom": "Formation IRIS", "salle": "Paris"}'
```

Check the output file from the host:

```bash
$ cat /irisdev/app/data/formation.txt
```

### 7.4. Polling CSV Service

Create `src/training/bs.py`:

```python
import csv
import os
from typing import Annotated

from iop import Category, PollingBusinessService, controls, setting, target
from training.msg import FormationRequest


class ReadCsvBs(PollingBusinessService):
    target = target(
        description="Component that receives each FormationRequest.",
    )
    filename: Annotated[str, setting(
        "formation.csv",
        category=Category.BASIC,
        description="CSV file name.",
    )]
    path: Annotated[str, setting(
        "/irisdev/app/misc/",
        category=Category.BASIC,
        description="Directory containing the CSV file.",
        control=controls.directory(),
    )]

    def on_poll(self):
        csv_path = os.path.join(self.path, self.filename)
        if not os.path.exists(csv_path):
            self.log_info(f"No CSV file to read: {csv_path}")
            return

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            next(reader, None)

            for row in reader:
                msg = FormationRequest(
                    id=int(row[0]),
                    nom=row[1],
                    salle=row[2],
                )
                self.send_request_sync(self.target, msg)
                self.log_info(f"FormationRequest {msg.id} sent to {self.target}")
```

The `target = target(...)` line declares a production port. The actual target is
set in `settings.py` with `prod.connect(...)`.

### 7.5. Connect The Pipeline

Replace `src/settings.py` with:

```python
from hello_world.bo import MyBo
from iop import Production
from training.bo import SaveInTxtBo
from training.bs import ReadCsvBs


prod = Production("MyIRIS.Production", testing_enabled=True)

my_bo = prod.operation("Instance.Of.MyBo", MyBo)
reader = prod.service("Instance.Of.ReadCsvBs", ReadCsvBs)
save_txt = prod.operation("Instance.Of.SaveInTxtBo", SaveInTxtBo)

prod.connect(reader.target, save_txt)

PRODUCTIONS = [prod]
```

Migrate and update:

```bash
% iop --migrate /irisdev/app/src/settings.py
% iop --update
```

You can inspect the Python-authored graph:

```bash
% iop --export MyIRIS.Production --format graph
```

Should show:

```text
MyIRIS.Production
  Instance.Of.MyBo [Python.helloworld.bo.MyBo]
  Instance.Of.ReadCsvBs [Python.training.bs.ReadCsvBs]
    target -> Instance.Of.SaveInTxtBo [inferred]
  Instance.Of.SaveInTxtBo [Python.training.bo.SaveInTxtBo]
```

Start or restart the production if needed:

```bash
% iop --status
% iop --start MyIRIS.Production --detach
```

If it is already running and you changed lifecycle code, restart it:

```bash
% iop --restart
```

### 7.6. Discover The UI

Production configuration:

http://localhost:52775/csp/irisapp/EnsPortal.ProductionConfig.zen?$NAMESPACE=IRISAPP

Message viewer:

http://localhost:52775/csp/irisapp/EnsPortal.MessageViewer.zen?$NAMESPACE=IRISAPP

Default credentials are:

- username: `SuperUser`
- password: `SYS`

The UI shows the production and message flow.

![UI](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/UI.jpg)

![MessageView](https://raw.githubusercontent.com/grongierisc/formation-template-python/main/misc/img/MessageView.jpg)

In v4, the UI is useful for inspection and runtime operations, but topology
should be kept in `src/settings.py` with the `Production` API.

Export the deployed production as Python:

```bash
% iop --export MyIRIS.Production --format python
```

This is useful for reverse engineering, but the source-of-truth file remains
your reviewed `src/settings.py`.

### 7.7. Exercise: Archive Processed Files

Modify `ReadCsvBs` so that after a CSV file is read, it is moved to an
`archive` folder.

One possible solution:

```python
import csv
import os
from typing import Annotated

from iop import Category, PollingBusinessService, controls, setting, target
from training.msg import FormationRequest


class ReadCsvBs(PollingBusinessService):
    target = target(
        description="Component that receives each FormationRequest.",
    )
    filename: Annotated[str, setting(
        "formation.csv",
        category=Category.BASIC,
        description="CSV file name.",
    )]
    path: Annotated[str, setting(
        "/irisdev/app/misc/",
        category=Category.BASIC,
        description="Directory containing the CSV file.",
        control=controls.directory(),
    )]
    archive_folder: Annotated[str, setting(
        "archive",
        category=Category.BASIC,
        description="Archive folder, relative to path.",
    )]

    def on_init(self):
        os.makedirs(os.path.join(self.path, self.archive_folder), exist_ok=True)

    def on_poll(self):
        csv_path = os.path.join(self.path, self.filename)
        if not os.path.exists(csv_path):
            self.log_info(f"No CSV file to read: {csv_path}")
            return

        with open(csv_path, newline="", encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            next(reader, None)

            for row in reader:
                msg = FormationRequest(
                    id=int(row[0]),
                    nom=row[1],
                    salle=row[2],
                )
                self.send_request_sync(self.target, msg)
                self.log_info(f"FormationRequest {msg.id} sent to {self.target}")

        archive_path = os.path.join(self.path, self.archive_folder)
        os.rename(csv_path, os.path.join(archive_path, self.filename))
        self.log_info(f"CSV file archived: {archive_path}")
```

After changing the code:

```bash
% iop --migrate /irisdev/app/src/settings.py
% iop --restart
```

Use restart here because the service lifecycle creates the archive directory in
`on_init`.

## 8. Part 2: Add A Process And PostgreSQL Operation

Now we add a business process. The service sends each CSV row to the process.
The process sends:

- the original `FormationRequest` to the text operation
- a transformed `TrainingInsertRequest` to the PostgreSQL operation

### 8.1. Add The Insert Message

Replace `src/training/msg.py` with:

```python
from dataclasses import dataclass

from iop import Message


@dataclass
class FormationRequest(Message):
    id: int = 0
    nom: str = ""
    salle: str = ""


@dataclass
class TrainingInsertRequest(Message):
    name: str = ""
    room: str = ""
```

### 8.2. Add The PostgreSQL Operation

Replace `src/training/bo.py` with:

```python
import os
from typing import Annotated

import psycopg2
from iop import BusinessOperation, Category, controls, setting
from training.msg import FormationRequest, TrainingInsertRequest


class SaveInTxtBo(BusinessOperation):
    filename: Annotated[str, setting(
        "formation.txt",
        category=Category.BASIC,
        description="Output file name.",
    )]
    path: Annotated[str, setting(
        "/irisdev/app/data/",
        category=Category.BASIC,
        description="Output directory.",
        control=controls.directory(),
    )]

    def on_init(self):
        os.makedirs(self.path, exist_ok=True)

    def on_formation_request(self, request: FormationRequest):
        output_file = os.path.join(self.path, self.filename)
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"{request.id};{request.nom};{request.salle}\n")

        self.log_info(f"FormationRequest {request.id} saved in {output_file}")


class PostgresOperation(BusinessOperation):
    host: Annotated[str, setting("db", category=Category.CONNECTION)]
    database: Annotated[str, setting("DemoData", category=Category.CONNECTION)]
    user: Annotated[str, setting("DemoData", category=Category.CONNECTION)]
    password: Annotated[str, setting("DemoData", category=Category.CONNECTION)]
    port: Annotated[int, setting(5432, category=Category.CONNECTION)]

    def on_init(self):
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password,
            port=self.port,
        )
        self.conn.autocommit = True

    def on_tear_down(self):
        self.conn.close()

    def on_training_insert_request(self, request: TrainingInsertRequest):
        sql = "INSERT INTO public.formation (name, room) VALUES (%s, %s)"
        with self.conn.cursor() as cursor:
            cursor.execute(sql, (request.name, request.room))

        self.log_info(f"Inserted training {request.name} in room {request.room}")
```

### 8.3. Add The Business Process

Create `src/training/bp.py`:

```python
from iop import BusinessProcess, target
from training.msg import FormationRequest, TrainingInsertRequest


class TrainingProcess(BusinessProcess):
    txt = target(description="Text file operation.")
    postgres = target(description="PostgreSQL operation.")

    def on_formation_request(self, request: FormationRequest):
        self.send_request_sync(self.txt, request)

        insert_request = TrainingInsertRequest(
            name=request.nom,
            room=request.salle,
        )
        return self.send_request_sync(self.postgres, insert_request)
```

The process owns routing decisions. The production graph owns which runtime item
each port points to.

### 8.4. Connect The Full Production

Replace `src/settings.py` with:

```python
from iop import Production
from training.bo import PostgresOperation, SaveInTxtBo
from training.bp import TrainingProcess
from training.bs import ReadCsvBs


prod = Production("MyIRIS.Production", testing_enabled=True)

reader = prod.service("Instance.Of.ReadCsvBs", ReadCsvBs)
process = prod.process("Instance.Of.TrainingProcess", TrainingProcess)
save_txt = prod.operation("Instance.Of.SaveInTxtBo", SaveInTxtBo)
postgres = prod.operation("Instance.Of.PostgresOperation", PostgresOperation)

prod.connect(reader.target, process)
prod.connect(process.txt, save_txt)
prod.connect(process.postgres, postgres)

PRODUCTIONS = [prod]
```

Migrate and update:

```bash
% iop --migrate /irisdev/app/src/settings.py
% iop --update
```

Inspect the graph:

```bash
% iop --export MyIRIS.Production --format graph
```

Expected shape:

```text
MyIRIS.Production
  Instance.Of.ReadCsvBs [Python.training.bs.ReadCsvBs]
    target -> Instance.Of.TrainingProcess [inferred]
  Instance.Of.TrainingProcess [Python.training.bp.TrainingProcess]
    postgres -> Instance.Of.PostgresOperation [inferred]
    txt -> Instance.Of.SaveInTxtBo [inferred]
  Instance.Of.SaveInTxtBo [Python.training.bo.SaveInTxtBo]
  Instance.Of.PostgresOperation [Python.training.bo.PostgresOperation]
```

Test the PostgreSQL operation directly:

```bash
% iop --test Instance.Of.PostgresOperation --classname training.msg.TrainingInsertRequest --body '{"name": "Formation IRIS", "room": "Paris"}'
```

Test the process:

```bash
% iop --test Instance.Of.TrainingProcess --classname training.msg.FormationRequest --body '{"id": 1, "nom": "Formation IRIS", "salle": "Paris"}'
```

Check PostgreSQL:

```bash
$ docker compose exec db psql -U DemoData -d DemoData -c "SELECT * FROM formation"
```

### 8.5. Compare Desired And Deployed Topology

The v4 `Production` object can compare your Python definition with what is
deployed in IRIS.

Inside an IRIS Python session or an IRIS-local script:

```python
from settings import prod

print(prod.graph())
print(prod.diff())
```

For command-line inspection:

```bash
% iop --export MyIRIS.Production --format json
% iop --export MyIRIS.Production --format python
% iop --export MyIRIS.Production --format graph
```

## 9. Useful v4 Commands

Run these inside the IRIS container unless you configure remote mode.

```bash
% iop --help
% iop --migrate /irisdev/app/src/settings.py --dry-run
% iop --migrate /irisdev/app/src/settings.py
% iop --start MyIRIS.Production --detach
% iop --status
% iop --update
% iop --restart
% iop --stop
% iop --queue MyIRIS.Production
% iop --log
% iop --log 20
% iop --bindings
% iop --bindings --unused
% iop --export MyIRIS.Production --format graph
```

Remote mode lets you run the CLI from the host against the IRIS web server:

```bash
$ export IOP_URL=http://localhost:52775
$ export IOP_USERNAME=SuperUser
$ export IOP_PASSWORD=SYS
$ export IOP_NAMESPACE=IRISAPP
$ iop --status
```

You can also store remote settings in `src/settings.py`:

```python
REMOTE_SETTINGS = {
    "url": "http://localhost:52775",
    "username": "SuperUser",
    "password": "SYS",
    "namespace": "IRISAPP",
    "verify_ssl": True,
}
```

Then run:

```bash
$ iop --status -R src/settings.py
$ iop --migrate src/settings.py -R src/settings.py
```

Use `--force-local` when you explicitly want to ignore remote settings and run
inside a local IRIS session.

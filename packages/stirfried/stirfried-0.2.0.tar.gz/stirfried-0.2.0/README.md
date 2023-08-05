[![PyPI version](https://badge.fury.io/py/stirfried.svg)](https://badge.fury.io/py/stirfried)
[![Docker Image Version (latest semver)](https://img.shields.io/docker/v/korijn/stirfried?label=docker%20image)](https://hub.docker.com/r/korijn/stirfried)

# Stirfried 🥡

Socket.IO server to schedule Celery tasks from clients in real-time.

## Getting started

Stirfried has a three layered architecture:

1. [Celery workers](#celery-workers)
2. [Socket.IO server](#socketio-server)
3. [Socket.IO clients](#socketio-clients)

### Installation

You really only need to install Stirfried in your Celery workers via pip:

 `pip install stirfried`

For the Socket.IO server component you can use the prebuilt docker image
`korijn/stirfried`, or you can copy the project and customize it to your
liking (there's only about 40 lines of code in the server).

Clients can connect using standard [Socket.IO](https://socket.io/) libraries.

### Celery workers

In your Celery workers, import the `StirfriedTask`:

```python
from stirfried.celery import StirfriedTask
```

Configure `StirfriedTask` as the base class globally:

```python
app = Celery(..., task_cls=StirfriedTask)
```

...or per-task:

```python
@app.task(base=StirfriedTask)
def add(x, y, room=None):
    return x + y
```

#### Rooms

The client passes the room to emit to via the keyword argument `room`.

The `StirfriedTask` base class depends on the presence of this keyword argument.

This means you are required to add the keyword argument `room=None` to your
task definitions in order to receive it.

It also gives the client control over whether the task results and progress
updates should be emitted to them or a certain room.

#### Progress

You can emit progress from tasks by calling `self.emit_progress(current, total)`.

Note that you are required to pass `bind=True` to the `celery.task` decorator
in order to get access to the `self` instance variable.

```python
@celery.task(bind=True)
def add(self, x, y, room=None):
    s = x
    self.emit_progress(50, 100)  # 50%
    s += y
    self.emit_progress(100, 100)  # 100%
    return s
```


### Socket.IO server

You are required to provide a `settings.py` file with the configuration
for the server.

It requires at a minimum:

* `socketio_redis` - Redis connection string for the [Socket.IO](https://github.com/miguelgrinberg/python-socketio) server.
* `broker_url` - Connection string for the [Celery](https://github.com/celery/celery/) [broker](http://docs.celeryproject.org/en/latest/getting-started/brokers/index.html).

The server sends tasks to the Celery broker
[by name](https://docs.celeryproject.org/en/latest/reference/celery.html#celery.Celery.send_task),
so it can act as a gateway to many different Celery workers with
different tasks. You can leverage Celery's
[task routing configuration](http://docs.celeryproject.org/en/latest/userguide/routing.html)
for this purpose.

#### Example

Let's say you have two workers, one listening on the `feeds` queue and
another on the `web` queue. This is how you would configure the 
server accordingly:

```python
socketio_redis = "redis://localhost:6379/0"
broker_url = "redis://localhost:6379/1"
task_routes = {
    "feed.tasks.*": {"queue": "feeds"},
    "web.tasks.*": {"queue": "web"},
}
```

#### Docker image

You can build the docker image and run it locally as follows (note that you need to create a `settings.py` file):

```bash
docker run --rm -ti -v `pwd`/settings.py:/app/settings.py:ro -p 8000:8000 stirfried
```

### Socket.IO clients

TODO

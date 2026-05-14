"""Patch Gunicorn's gthread worker.

This module revert changes applied in version 21.0.0 https://github.com/benoitc/gunicorn/pull/2918.

Users who used Gunicorn without a reverse proxy faced the problem of server blocking.
In short, when clients establish speculative TCP connections without sending data,
threads are blocked on the recv() operation.
When such connections exceed the number of threads, the server stops processing requests.
For more explanation read the issue https://github.com/benoitc/gunicorn/issues/2917.

Since version 21.0.0, the recv() operation only occurs when the socket has received data.
The server sets the block only on those connections through which the client sends data.

The consequences.
When a client connect to server, the worker accepts the connection, and registers callback with the poller.
If the worker is currently processing another request, and the request number is greater than ``max-requests`` option,
the worker will automatically restart.
After the process completes, all accepted connections are closed.
When the client sends data, the error "Connection reset by peer" occurs and 502 status code is returned.
For more explanation read the issue https://github.com/benoitc/gunicorn/issues/3038.

The fixes.
Revert changes applied in version 21.0.0.
Set a lock on the connection and immediately pass the request handler to the thread pool.
Disable logic with ``initialized`` variable.

Usage:
    Use ``--worker-class`` option in cli, or ``worker_class`` in config file.

        $ gunicorn --worker-class gunicorn_worker.ThreadWorkerSync

"""

import errno

from gunicorn import SERVER_SOFTWARE, version_info
from gunicorn.workers.gthread import TConn, ThreadWorker

COMPATIBLE = False

if (21, 0, 0) <= version_info <= (23, 0, 0):
    COMPATIBLE = True

if not COMPATIBLE:
    raise RuntimeError(f'{SERVER_SOFTWARE} is not supported')


class TConnSync(TConn):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initialized = True


class ThreadWorkerSync(ThreadWorker):

    def accept(self, server, listener):
        try:
            sock, client = listener.accept()
            # initialize the connection object
            conn = TConnSync(self.cfg, sock, client, server)

            self.nr_conns += 1
            # wait until socket is readable
            self.enqueue_req(conn)

        except OSError as e:
            if e.errno not in (
                errno.EAGAIN,
                errno.ECONNABORTED,
                errno.EWOULDBLOCK,
            ):
                raise

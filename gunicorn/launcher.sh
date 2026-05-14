#!/bin/sh

gunicorn "$@" &

GUNICORN_PID=$!
GUNICORN_DELAYED_SHUTDOWN=${GUNICORN_DELAYED_SHUTDOWN:-5}

delayed_shutdown() {
    sleep ${GUNICORN_DELAYED_SHUTDOWN}
    kill -TERM "$GUNICORN_PID"
    wait "$GUNICORN_PID"
    exit 0
}

trap delayed_shutdown TERM

wait "$GUNICORN_PID"

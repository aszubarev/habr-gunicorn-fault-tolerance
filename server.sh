#!/bin/sh

set -o errexit
set -o nounset

if [ -d /tmp/nginx ]; then
  echo "/tmp/nginx directory exists."
else
  echo "/tmp/nginx does not exists. Create manually."
  mkdir -p /tmp/nginx
fi

if [ -d /tmp/gunicorn ]; then
  echo "/tmp/gunicorn directory exists."
else
  echo "/tmp/gunicorn does not exists. Create manually."
  mkdir -p /tmp/gunicorn
fi

echo "supervisor starting..."
exec supervisord -c /etc/supervisor/conf.d/server.cfg -n

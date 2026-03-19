PWD := $(shell pwd)

run_local_nginx:
	@nginx -g "daemon off;" -c ${PWD}/nginx/local.conf

run_local_app_5:
	@gunicorn wsgi:app --bind 127.0.0.1:8000 --control-socket /tmp/gunicorn.ctl -w 5

run_local_app_6:
	@gunicorn wsgi:app --bind 127.0.0.1:8000 --control-socket /tmp/gunicorn.ctl -w 6

run_local_app_10:
	@gunicorn wsgi:app --bind 127.0.0.1:8000 --control-socket /tmp/gunicorn.ctl -w 10

run_unix_nginx:
	@nginx -g "daemon off;" -c ${PWD}/nginx/unix.conf

run_unix_app_5:
	@gunicorn wsgi:app --bind unix:/tmp/gunicorn.sock --control-socket /tmp/gunicorn.ctl -w 5

run_unix_app_6:
	@gunicorn wsgi:app --bind unix:/tmp/gunicorn.sock --control-socket /tmp/gunicorn.ctl -w 5
PWD := $(shell pwd)

run_nginx:
	@nginx -g "daemon off;" -c ${PWD}/nginx.conf

run_app:
	@gunicorn wsgi:app --bind unix:/tmp/gunicorn.sock --control-socket /tmp/gunicorn.ctl -w 1
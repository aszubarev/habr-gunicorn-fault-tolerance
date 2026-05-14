PWD := $(shell pwd)

run_nginx:
	@nginx -g "daemon off;" -c ${PWD}/nginx.conf -e /dev/stdout

run_app:
	@gunicorn wsgi:app --bind 127.0.0.1:8000 -w 2 -k gthread --threads 2 --max-requests 4 --max-requests-jitter 4 --keep-alive 30

user = 'user-app'
group = 'group-app'

bind = ['127.0.0.1:5000']
backlog = 1024

pythonpath = '/etc'
workers = 2
worker_class = 'gthread'
worker_connections = 1024
worker_tmp_dir = '/tmp/gunicorn'
keepalive = 10
threads = 5

max_requests = 1000
max_requests_jitter = 10000

control_socket_disable = True

graceful_timeout = 10

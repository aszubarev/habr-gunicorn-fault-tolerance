DOCKER_ID_NGINX := $(shell docker ps -f name=0-fixed-by-separate-networks_nginx -q)
DOCKER_ID_APP := $(shell docker ps -f name=0-fixed-by-separate-networks_app -q)

exec_nginx:
	@docker exec -it ${DOCKER_ID_NGINX} bash

exec_app:
	@docker exec -it ${DOCKER_ID_APP} bash

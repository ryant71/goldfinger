.PHONY: list

list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$'

build-app:
	docker build -t dash goldfinger

run-app:
	docker run --publish 8050:8050 --name dash --rm dash

stop-app:
	docker stop dash

attach-app:
	docker exec -it dash bash

test-app:
	docker exec -it dash 'curl localhost'

build-redis:
	docker build -t redis redis


.PHONY: build stop attach

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


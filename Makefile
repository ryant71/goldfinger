.PHONY: build stop attach

build:
	docker build -t myapp .

run:
	docker run --publish 8050:8050 --name myapp --rm myapp

stop:
	docker stop myapp

attach:
	docker exec -it myapp bash

test:
	docker exec -it myapp 'curl localhost'

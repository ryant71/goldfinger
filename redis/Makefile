
up:
	docker-compose up --build -d

down:
	docker-compose down

cli:
	docker run -it --network redis_node_net --rm redis redis-cli -h redis

attach:
	docker exec -it redis_redis_1 sh

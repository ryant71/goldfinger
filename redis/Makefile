
up:
	docker-compose up --build -d --rm

down:
	docker-compose down

cli:
	docker run -it --network redis_node_net2 --rm redis redis-cli -h redis

gf-cli:
	docker run -it --network goldfinger_node_net --rm redis redis-cli -h redis

attach:
	docker exec -it redis_redis_1 sh

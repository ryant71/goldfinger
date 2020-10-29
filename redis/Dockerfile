FROM redis:alpine

COPY redis-data/ /data/
COPY redis.conf /usr/local/etc/redis/redis.conf

ENV REDIS_REPLICATION_MODE master

EXPOSE 6379

CMD ["redis-server"]

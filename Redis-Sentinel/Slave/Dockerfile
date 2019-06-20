FROM redis:5-alpine
COPY redis-slave.conf /usr/local/etc/redis/redis.conf
COPY sentinel.conf /usr/local/etc/redis/sentinel.conf
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]

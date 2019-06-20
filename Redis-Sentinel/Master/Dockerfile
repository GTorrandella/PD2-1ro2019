FROM redis:5-alpine
COPY redis-master.conf /usr/local/etc/redis/redis.conf
COPY sentinel.conf /usr/local/etc/redis/sentinel.conf
COPY example.txt example.txt
CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]

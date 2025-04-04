#!/bin/sh
# redis-entrypoint.sh

# Run the initialization script
#sh /data/redis-init.sh

# Start Redis server
#exec redis-server --bind 0.0.0.0

# Start Redis server in the background
redis-server --bind 0.0.0.0 &

# Wait for Redis to be ready
while ! redis-cli ping > /dev/null 2>&1; do
  echo "Waiting for Redis to be ready..."
  sleep 1
done

# Run the initialization script
sh /data/redis/redis-init.sh

# Wait for the Redis server process
wait

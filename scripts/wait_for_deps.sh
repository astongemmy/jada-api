#!/bin/sh

set -e

until redis-cli -h redis ping | grep -q "PONG" ; do
  >&2 echo "Redis is unavailable - retrying"
  sleep 5
done

>&2 echo "[Redis] is up - executing command"

exec "$@"

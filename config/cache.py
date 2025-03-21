from config.common import IS_DEVELOPMENT
import redis


AuthToken = redis.Redis(
  decode_responses=IS_DEVELOPMENT,
  host='localhost',
  port=6379,
  db=0
)
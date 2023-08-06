# your package information
import config

name = "greendeck-redis"
__version__ = config.get_greendeck_redis_version()
author = "Yashvardhan Srivastava"
author_email = "yash@greendeck.co"
url = ""

# import sub packages
from .src.redis.redis import Redis
from .src.redis.redis import RedisSet
from .src.redis.redis import RedisQueue

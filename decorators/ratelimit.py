from functools import wraps
from services.redis_bucket import RedisBucket
import redis

client = redis.Redis("localhost", 6379, 0, decode_responses=True)



def login_rate_limiter(request):
    token_bucket = RedisBucket(client)
    def decorator(f):
        @wraps(f)
        def wrapper_function(*args, **kwargs):

            return f(*args, **kwargs)
        return wrapper_function

    return decorator








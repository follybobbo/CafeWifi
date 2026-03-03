from functools import wraps
from flask import request, jsonify
from services.redis_bucket import RedisBucket
import redis

client = redis.Redis("localhost", 6379, 0, decode_responses=True)




def login_token_bucket_limiter(limit, rate):
    token_bucket = RedisBucket(client)
    def decorator(f):
        @wraps(f)
        def wrapper_function(*args, **kwargs):
            user_ip = request.remote_addr
            key = f"id: {user_ip}"
            redis_response = token_bucket.run_redis_script(key=key, bucket_capacity=limit, rate_of_refill=rate, token_per_request=1)
            token_left = redis_response[0]
            request_allowed = redis_response[1]


            if not request_allowed:
                response = jsonify({"error": "Too many request"})
                response.status_code = 429


            response = f(*args, **kwargs)
            response.headers["X-RateLimit-Remaining"] = f"{int(request_allowed)}"
            return response

        return wrapper_function

    return decorator








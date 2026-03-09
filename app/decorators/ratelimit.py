from functools import wraps
from flask import request, jsonify
from app.services.redis_token_bucket_service import RedisBucket
import redis

client = redis.Redis("localhost", 6379, 1, decode_responses=True)




def login_token_bucket_limiter(limit: int, rate: int):
    token_bucket = RedisBucket(client)
    def decorator(f):
        @wraps(f)
        def wrapper_function(*args, **kwargs):
            if request.method == "POST":
                #if request is post give client use rate limiter
                print("Login done---post")
                user_ip = request.remote_addr
                key = f"id: {user_ip}"
                redis_response = token_bucket.run_redis_script(key=key, bucket_capacity=limit, rate_of_refill=rate, token_per_request=1)
                token_left = redis_response[0]
                request_allowed = redis_response[1]


                if not request_allowed:
                    response = jsonify({"error": "Too many request"})
                    response.headers["Retry-After"] = "1 second"
                    response.status_code = 429

                print(token_left)
                response = f(*args, **kwargs)
                response.headers["X-RateLimit-Limit"] = limit
                response.headers["X-RateLimit-Remaining"] = f"{int(token_left)}"
                return response
            elif request.method == "GET":
                #if request is GET give client page resource
                print("Login done -----get")
                return f(*args, **kwargs)
        return wrapper_function

    return decorator








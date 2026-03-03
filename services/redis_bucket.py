import redis
from typing import Tuple


lua_script = """
 --get all keys and variable sent to script.
 local key = KEYS[1]
 local bucket_capacity = ARGV[1]
 local rate_of_refill = ARGV[2]
 local token_per_request = ARGV[3]
 local token
 
 --get redis time returns list of time, first item in seconds, second item in micro seconds
 local time_data = redis.call("TIME")
 local time_now_in_seconds = tonumber(time_data[1]) + (tonumber(time_data[2])/1000000)
 
 local bucket = redis.call("HMGET", key, "token_saved", "last_refill_time")
 local elapsed
 local last_bucket_refill_time
 
 
 --refill block
 
 --used or not and in order to prevent errors that arises from partial state write
 
 --first conditional block runs on first request
 --second conditional block runs subsequently
 if not bucket[1] or not bucket[2] then
   token = bucket_capacity
   last_bucket_refill_time = time_now_in_seconds
   elapsed = 0
 else
   token = tonumber(bucket[1])
   last_bucket_refill_time = tonumber(bucket[2])
   
   elapsed = time_now_in_seconds - last_bucket_refill_time
   
   local token_to_add = rate_of_refill * elapsed
   token = math.min(bucket_capacity, token + token_to_add)
   last_bucket_refill_time = time_now_in_seconds 
 end
 
 --define request allowed equals false
 local request_allowed = 0
 
 --token usage block
 if token >= token_per_request then 
   token = token - token_per_request
   request_allowed = 1
 end
 
 redis.call("HMSET", key, "token_saved", token, "last_refill_time", last_bucket_refill_time)
 
 --clear redis of any users bucket who does not make an request after time to fill bucket times 2
 local time_to_fill_bucket = bucket_capacity/rate_of_refill
 redis.call("EXPIRE", key, time_to_fill_bucket * 2)
 
 return {token, request_allowed}
"""


class RedisBucket:

    def __init__(self, redis_client: redis.Redis):
        self.client = redis_client
        self.script = self.client.register_script(lua_script)



    def run_redis_script(self, key, bucket_capacity: int, rate_of_refill: int, token_per_request: int)-> Tuple[int, bool]:
        response = self.script(keys=[key], args=[bucket_capacity, rate_of_refill, token_per_request])

        token_left = response[0]
        is_request_allowed = response[1]

        return token_left, is_request_allowed


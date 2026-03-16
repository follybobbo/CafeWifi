# from app.services import
import redis
from app.services import redis_client

# LUA_BACKOFF_SCRIPT = """
#     local key = KEYS[1]
#     local cool_off_period
#     local counter_value
#     local user_banned
#     local data
#
#
#     data = redis.call("HMGET", key, "counter_value", "user_banned")
#     counter_value = tonumber(data[1]) or 0
#
#     cool_off_period = redis.call("EXISTS", "cool_off_period")
#     user_banned = 0
#
#
#     if cool_off_period == 0 then
#       counter_value = counter_value + 1
#       if counter_value == 3 then
#          redis.call("SET", "cool_off_period", "1", "EX", 11)
#       elseif counter_value == 6 then
#         redis.call("SET", "cool_off_period", "1", "EX",30)
#       elseif counter_value > 6 then
#         user_banned = 1
#       end
#     end
#
#     redis.call("HMSET", key, "counter_value", tonumber(counter_value), "user_banned", tonumber(user_banned))
#     return {cool_off_period, counter_value, user_banned}
# """

lua_better = """
  local user_key = KEYS[1]
  
  --atomic increment used to increase user key read, update and write all done at once
  local failed_attempt = redis.call("INCR", user_key)
  
  --delay value is exponential
  local delay = math.min(2^failed_attempt, 300)
  
  --cooldown key is stored for delay seconds, so state can be checked in view function
  redis.call("SET", user_key..":cooldown", 1, "EX", delay)
  
  --after 60 minutes delete user key from blacklist
  redis.call("EXPIRE", user_key, 3600)
  
  return {failed_attempt, delay}
"""


class BackOff:
    def __init__(self, redis_client: redis.Redis):
        self.client = redis_client
        self.script = self.client.register_script(lua_better)




    def start_back_off(self, key)-> tuple[int, int]:

        result = self.script(keys=[key])


        failed_attempt = int(result[0])
        delay = int(result[1])
        # is_user_banned = bool(result[2])

        return failed_attempt, delay

    def delete_black_list_record(self, user_key):
        self.client.delete(user_key)


# redis_client = create_redis_client_instance(3)

#
# def do_the_stuff(user_name_key: str)-> tuple[bool, int, bool]:
#
#
#     result = back_off.start_back_off(user_name_key)
#
#     is_cool_off_period = result[0]
#     failed_login_counter = result[1]
#     is_user_banned = result[2]
#
#     return is_cool_off_period, failed_login_counter, is_user_banned


import redis



redis_client = redis.Redis(
    host="localhost",
    port=6379,
    db=0,
    decode_responses=True
)


#
# def create_redis_client_instance(db_number: int):
#     redis_client = redis.Redis(
#         host="localhost",
#         port=6379,
#         db=db_number,
#         decode_responses=True
#     )
#
#     return redis_client


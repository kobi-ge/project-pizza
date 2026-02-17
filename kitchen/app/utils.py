
def delete_from_redis(order_id, redis):
    return redis.delete(order_id)

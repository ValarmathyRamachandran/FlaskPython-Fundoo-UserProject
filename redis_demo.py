import redis

redis_host = 'localhost'
redis_port = 6379

r = redis.Redis(
    host=redis_host,
    port=redis_port,
    decode_responses=True)


def redis_string():
    try:

        r.set("msg", "Hello Everyone")
        msg = r.get("msg")
        return {"msg": msg}
    except Exception as e:
        return e


def redis_integer():
    try:

        r.set("number", "100")
        original_num = r.get("number")
        r.incr("number")
        incr_num = r.get('number')
        return {"msg": (original_num, incr_num)}
    except Exception as e:
        return e


if __name__ == "__main__":
    string = redis_string()
    integer = redis_integer()
    print(string)
    print(integer)

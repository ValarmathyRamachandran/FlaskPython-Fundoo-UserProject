import redis

redis_host = 'localhost'
redis_port = 6379


def redis_string():
    try:
        r = redis.Redis(
            host=redis_host,
            port=redis_port,
            decode_responses=True)
        r.set("msg", "Hello Everyone")
        msg = r.get("msg")
        print(msg)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    redis_string()

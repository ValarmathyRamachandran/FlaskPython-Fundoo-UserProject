import json
import jwt
import redis
from flask import request
from user.models import Users

r = redis.Redis(
    host='localhost',
    port=6379
)


def token_required(f):
    def decorated(*args, **kwargs):
        # print(**kwargs)
        token = None
        # jwt is passed in the request header
        print(request.headers)
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return {'message': 'Token is missing !!', 'code': 401}

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, '7f64ce34f65257f16d15608f947c3a7c', "HS256")
            current_user = Users.objects.get(email=data['email'])
            user = {'user': current_user}
        except Exception as e:
            return {
                'message': 'Token is invalid !!', 'code': 401
            }
        # returns the current logged in users contex to the routes
        return f(*args, **user)

    return decorated


def set_cache(key, value, expire_time):
    json_dict = json.dumps(value)
    r.set(key, json_dict)
    r.expire(key, expire_time)


def get_cache(key):
    value = r.get(key)
    return value

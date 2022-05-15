import datetime
import jwt
from flask import request, jsonify, app
from user.models import Users


def generate_token(mail, Secret):
    return jwt.encode({'email': mail, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                      Secret, algorithm="HS256")


def token_required(f):
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return {'msg': 'Token is missing !!', 'code': 401}

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], "HS256")
            current_user = Users.objects.get(email=data['email'])
        except Exception as e:
            return {'msg': 'Token is invalid !!', 'code': 402}
        # returns the current logged-in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated

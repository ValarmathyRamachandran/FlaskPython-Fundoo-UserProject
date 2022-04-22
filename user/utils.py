# decorator for verifying the JWT
import datetime

import jwt
from flask import request, jsonify, app
import user

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
            return jsonify({'message': 'Token is missing !!'}), 401

        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'], "HS256")
            current_user = Users.objects.get(email=data['email'])
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return f(current_user, *args, **kwargs)

    return decorated

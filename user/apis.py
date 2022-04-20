import json
import jwt
from flask import request, app, Flask, jsonify
from flask_restful import Resource
import datetime

import send_email
from user.models import Users
from user.utils import token_required

app = Flask(__name__)
app.config['SECRET_KEY'] = '7f64ce34f65257f16d15608f947c3a7c'


class Registration(Resource):

    def post(self):
        """
        post api is for user registration for this app
        :return: message after validations for adding new user
        """
        req_data = request.data
        record = json.loads(req_data)

        del record['confirm_password']
        user = Users(id=record['id'], first_name=record['first_name'], last_name=record['last_name'],
                     user_name=record['user_name'], email=record['email'], password=record['password'])
        user.save()
        return {'msg': 'User Registered successfully'}, 200


# api.add_resource(Registration, '/registration')


class Login(Resource):
    """
     Flask-restful resource for retrieving user info.
    """

    def get(self):
        req_data = request.get_json()
        user = Users.objects.get(email=req_data.get('email'))

        if user is None:
            return {'msg': 'No user found'}
        else:
            if user.password == req_data.get('password'):
                token = jwt.encode(
                    {'email': user.email, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                    app.config['SECRET_KEY'], "HS256")

                return {'msg': 'password matches', 'status code': 200, 'token': token}

            return {'msg': 'password didnot match'}


# api.add_resource(Login, '/login')

class AccountActivation(Resource):
    @token_required
    def get(self, *args, **kwargs):
        req_data = request.get_json()
        user = Users.objects.get(email=req_data.get('email'))
        print(*args, **kwargs)
        return {'msg': 'sent email to user'}

import json
from datetime import datetime
import jwt
from flask import request, app
from flask_restful import Resource
from user.models import Users


class Registration(Resource):

    def post(self):
        """
        post api is for user registration for this app
        :return: message after validations for adding new user
        """
        req_data = request.data
        record = json.loads(req_data)

        del record['confirm_password']
        user = Users(**record)
        user.save()
        return {'msg': 'User Registered successfully'}, 200


#api.add_resource(Registration, '/registration')


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


#api.add_resource(Login, '/login')


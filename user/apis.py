import json
import jwt
from flask import request, app, Flask, jsonify
from flask_restful import Resource
import datetime
from send_email import send_email

from user.models import Users
from user.utils import token_required, generate_token

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
        if Users.objects.filter(email=user.email):
            return {'msg': 'User Already exists'}
        user.save()
        token = generate_token(user.email, app.config['SECRET_KEY'])
        send_email(user.email, "Account Activation", "Hi, Your Account has been Registered Successfully! "
                                                     "\n Please Click the below link to activate your account  "
                                                     "\n http://127.0.0.1:4040/activation?activate=",
                   token)
        return {'msg': 'User Registered successfully'}, 200


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
                token = generate_token(user.email, app.config['SECRET_KEY'])
                return {'msg': 'password matches', 'status code': 200, 'token': token}

            return {'msg': 'password didnot match'}


class AccountActivation(Resource):
    """
    Flask-restful resource for activating user account.
    """

    def get(self, *args, **kwargs):
        token = request.args.get('activate')
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
        user = Users.objects.get(email=payload.get('email'))
        if user is None:
            return {'msg': 'No users found'}
        if not user.is_active:
            user.is_active = True
            user.save()
            return {'msg': 'Acct activated successfully'}
        else:
            return {'msg': 'Acct has been already activated'}
        print(payload)

        print(*args, **kwargs)
        return {'msg': payload}


class ForgotPassword(Resource):
    def get(self, *args, **kwargs):
        req_data = request.get_json()
        user = Users.objects.get(email=req_data.get('email'))

        token = generate_token(user.email, app.config['SECRET_KEY'])
        send_email(user.email, "Forgot password", "Hi, Please click the below link to reset your password "
                                                  " \n http://127.0.0.1:4040/resetpassword?reset=", token)
        return {'msg': 'sent email to user along with reset link'}


class ResetPassword(Resource):
    def get(self, *args, **kwargs):
        token = request.args.get('reset')
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
        req_data = request.get_json()
        user = Users.objects.get(email=payload.get('email'))

        if user is None:
            return {'msg': 'No users found'}
        if user.is_active:
            user.password = req_data.get("new_password")
            user.save()
            return {'msg': 'password was changed successfully'}

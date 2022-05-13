import json
import jwt
from flask import request, app, Flask, jsonify, render_template
from flask_restful import Resource
from tasks import send_email
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
        user = Users(first_name=record['first_name'], last_name=record['last_name'],
                     user_name=record['user_name'], email=record['email'], password=record['password'])
        if Users.objects.filter(email=user.email):
            return {'msg': 'User Already exists', 'code': 409}
        user.save()
        token = generate_token(user.email, app.config['SECRET_KEY'])
        template = render_template('activation_template.html', token=token)
        # send_email(user.email, "Account Activation", "Hi, Your Account has been Registered Successfully! "
        # "\n Please Click the below link to activate your account  "
        # "\n http://127.0.0.1:4040/activation?activate=",
        # token)
        send_email.sleep(user.email, "Account Activation", template, token)

        return {'msg': 'User Registered successfully', 'code': 201}


class Login(Resource):
    """
     Flask-restful resource for retrieving user info.
    """

    def get(self):

        req_data = request.get_json()
        user = Users.objects.get(email=req_data.get('email'))

        if user is None:
            return {'msg': 'User not found', 'code': 404}
        else:
            if user.password == req_data.get('password'):
                token = generate_token(user.email, app.config['SECRET_KEY'])
                return {'msg': 'Login success', 'code': 200, 'token': token}

            return {'msg': 'password didnot match', 'code': 401}


class AccountActivation(Resource):
    """
    Flask-restful resource for activating user account.
    """

    def get(self, *args, **kwargs):
        token = request.args.get('activate')
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
        user = Users.objects.get(email=payload.get('email'))
        if user is None:
            return {'msg': 'User not found', 'code': 404}
        if not user.is_active:
            user.is_active = True
            user.save()
            return {'msg': 'Account activated successfully', 'code': 200}

        else:
            return {'msg': 'Account has been already activated', 'code': 409}


class ForgotPassword(Resource):
    def get(self, *args, **kwargs):
        req_data = request.get_json()
        user = Users.objects.get(email=req_data.get('email'))

        token = generate_token(user.email, app.config['SECRET_KEY'])
        send_email(user.email, "Forgot password", "Hi, Please click the below link to reset your password "
                                                  " \n http://127.0.0.1:4040/resetpassword?reset=", token)
        return {'msg': 'sent email to user along with reset link', 'code': 200}


class ResetPassword(Resource):
    def get(self, *args, **kwargs):
        token = request.args.get('reset')
        payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
        req_data = request.get_json()
        user = Users.objects.get(email=payload.get('email'))

        if not user:
            return {'msg': 'Users Not found', 'code': 404}
        if user.is_active:
            user.password = req_data.get("new_password")
            user.save()
            return {'msg': 'password was changed successfully', 'code': 200}
        return {'msg': 'User is inactive', 'code': 403}

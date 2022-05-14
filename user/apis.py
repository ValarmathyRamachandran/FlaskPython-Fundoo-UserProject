import json, jwt
from flask import request, app, Flask, render_template
from flask_restful import Resource
from flask_restful_swagger import swagger

from common import logger
from common.exception import PasswordMismatched, AlreadyExist, NotExist
from tasks import send_email
from user.models import Users
from user.utils import generate_token

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'


class Registration(Resource):
    @swagger.model
    @swagger.operation(notes='swagger is working')
    def post(self):

        """
        post api is build for user registration of this app
        :return: message once user is added along with registered email to activate account
        """

        req_data = request.data
        record = json.loads(req_data)
        first_name = record.get('first_name')
        last_name = record.get('last_name')
        user_name = record.get('user_name')
        email = record.get('email')
        password = record.get('password')
        confirm_password = record.get('confirm_password')

        if not confirm_password == password:
            return {'msg': 'Password and confirm Password must be same', 'code': 409}

        del record['confirm_password']
        user = Users(first_name, last_name, user_name, email, password)

        if Users.objects.filter(email=user.email):
            return {'msg': 'User Already exists', 'code': 409}
        else:
            try:
                token = generate_token(user.email, app.config['SECRET_KEY'])
                template = render_template('activation_template.html', token=token)
                send_email.sleep(user.email, "Account Activation", template, token)
                user.save()
                return {'msg': 'User Registered successfully', 'code': 201}
            except Exception as e:
                logger.logging.error('Log Error Message', e)
                return {'Error': 'Something went wrong', 'code': 500}


class Login(Resource):
    """
     This api is used to log in user with correct login credentials
     @return:User logged in successful msg if login credentials matches
    """

    @swagger.model
    @swagger.operation(notes='swagger is working')
    def get(self):

        req_data = request.get_json()
        user = Users.objects.get(email=req_data.get('email'))

        if user is None:
            return {'msg': 'User not found', 'code': 404}
        else:
            try:
                if user.password == req_data.get('password'):
                    token = generate_token(user.email, app.config['SECRET_KEY'])
                    return {'msg': 'Login success', 'code': 200, 'token': token}
            except PasswordMismatched as e:
                return {'msg': 'password didnot match', 'code': 401}


class AccountActivation(Resource):
    """
    This api is build to activate user account,
    once user enters the link registered email
    @return: Account activated successfully msg if it meets the condition
    """

    @swagger.model
    @swagger.operation(notes='swagger is working')
    def get(self):
        try:
            token = request.args.get('activate')
            payload = jwt.decode(token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
            user = Users.objects.get(email=payload.get('email'))
            if user is None:
                return {'msg': 'User not found', 'code': 404}
            if not user.is_active:
                user.is_active = True
                user.save()
                return {'msg': 'Account activated successfully', 'code': 200}
        except AlreadyExist as e:
            return {'msg': 'Account has been already activated', 'code': 409}


class ForgotPassword(Resource):
    @swagger.model
    @swagger.operation(notes='swagger is working')
    def get(self):
        """
        this api is used to send reset link to the user email
        :return:whether user receives an email or not on entered email id to reset the password
        """
        req_data = request.get_json()
        user = Users.objects.get(email=req_data.get('email'))
        try:
            if not user:
                raise NotExist("user Not found ", 404)

            token = generate_token(user.email, app.config['SECRET_KEY'])
            send_email(user.email, "Forgot password", "Hi, Please click the below link to reset your password "
                                                      " \n http://127.0.0.1:4040/resetpassword?reset=", token)
            return {'msg': 'sent email to user along with reset link', 'code': 200}
        except Exception as exception:
            return {"msg": exception.Error, 'code': exception.code}


class ResetPassword(Resource):
    @swagger.model
    @swagger.operation(notes='swagger is working')
    def get(self):
        """
        This api is used to Change password
        :return: password was changed successfully or not
        """
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

from flask import Flask
from flask_restful import Api
from db.utils import connect_db
from dotenv import load_dotenv
from routes import all_routes
from flask_restful_swagger import swagger

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/docs')


def config_app_routes():
    for route in all_routes:
        api_class = route[0]
        end_point = route[1]
        api.add_resource(api_class, end_point)


config_app_routes()
connect_db()

if __name__ == '__main__':
    app.run(debug=True, port=4040)



from flask import app, request, Flask, Response, jsonify, make_response
from flask_restful import Resource, Api, abort
from db.utils import connect_db
from routes import all_routes


app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = '7f64ce34f65257f16d15608f947c3a7c'


def config_app_routes():
    for route in all_routes:
        end_point = route[0]
        handler = route[1]
        api.add_resource(handler, end_point)


config_app_routes()
connect_db()

if __name__ == '__main__':
    app.run(debug=True, port=4040)

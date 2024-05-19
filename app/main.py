from flasgger import Swagger
from flask import Flask
from numpy import loadtxt
from tensorflow.keras.models import load_model
from app.config import config
from app.controllers.car import create_car_controller
from app.controllers.swagger import create_swagger_controller
from app.database.database import Database
from app.repositories.car import CarRepository
from app.repositories.damage import CarDamageRepository
from app.services.car import CarService


def create_app(config_name):
    db = Database()
    session = db.get_session()

    flask = Flask(__name__)
    flask.config.from_object(config[config_name])
    car_repository = CarRepository(session)
    damage_repository = CarDamageRepository(session)
    car_service = CarService(car_repository,damage_repository)
    car_controller = create_car_controller(car_service)

    flask.register_blueprint(car_controller, url_prefix='/api')

    swagger_config = {
        "specs": [
            {
                "endpoint": 'add_car',
                "route": '/add_car.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
                "yaml": True,  # Set to True if using YAML files
                "swagger": True,  # Set to True if using Swagger UI
                # "validation": True  # Set to True if using validation
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/",
        # Define the directory where YAML files are located
        # "specs_dir": "/home/mohammad/Desktop/chal/app/swagger",
        # Add headers configuration
        "headers": [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE'),
            ('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        ]
    }

    Swagger(flask, config=swagger_config)

    return flask


if __name__ == "__main__":
    app = create_app('development')
    app.run(port=5002)

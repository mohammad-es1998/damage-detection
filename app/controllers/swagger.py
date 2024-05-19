from flask import Blueprint
from flasgger import Swagger


def create_swagger_controller():
    swagger_blueprint = Blueprint('swagger', __name__)
    swagger = Swagger()

    @swagger_blueprint.route('/swagger')
    def show_swagger():
        return swagger.swagger_static()

    return swagger_blueprint

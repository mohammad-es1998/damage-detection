from flask import Blueprint, jsonify, request, send_file
from flasgger import Swagger, swag_from
from app.controllers.response import ResponseConstants
from app.services.car import CarService


def create_car_controller(car_service: CarService):
    car_controller = Blueprint('car_controller', __name__)


    @car_controller.route('/add_car', methods=['POST'])
    @swag_from('swagger/add_car.yml', methods=['POST'])
    def add_car():
        try:
            data = request.json
            car_service.add_car(data)
            return jsonify(ResponseConstants.ok("Car added successfully")), 201
        except Exception as e:
            print(f"Error occurred while adding car: {e}")
            return jsonify(ResponseConstants.internal_error()), 500

    @car_controller.route('/update_car/<plate>', methods=['PUT'])
    @swag_from('swagger/update_car.yml')
    def update_car(plate):
        try:
            data = request.json
            data['plate'] = plate
            car_service.update_car(data)
            return jsonify(ResponseConstants.ok("Car updated successfully")), 200
        except Exception as e:
            print(f"Error occurred while updating car: {e}")
            return jsonify(ResponseConstants.internal_error()), 500

    @car_controller.route('/delete_car/<plate>', methods=['DELETE'])
    @swag_from('swagger/delete_car.yml')
    def delete_car(plate):
        try:
            car_service.delete_car(plate)
            return jsonify(ResponseConstants.ok("Car deleted successfully")), 200
        except Exception as e:
            print(f"Error occurred while deleting car: {e}")
            return jsonify(ResponseConstants.internal_error()), 500

    @car_controller.route('/add_damage', methods=['POST'])
    @swag_from('swagger/add_damage.yml')
    def add_damage():
        try:
            data = request.json
            car_service.add_damage(data)
            return jsonify(ResponseConstants.ok("Damage added successfully")), 201
        except Exception as e:
            print(f"Error occurred while adding damage: {e}")
            return jsonify(ResponseConstants.internal_error()), 500

    @car_controller.route('/update_damage/<damage_id>', methods=['PUT'])
    @swag_from('swagger/update_damage.yml')
    def update_damage(damage_id):
        try:
            data = request.json
            data['id'] = damage_id
            car_service.update_damage(data)
            return jsonify(ResponseConstants.ok("Damage updated successfully")), 200
        except Exception as e:
            print(f"Error occurred while updating damage: {e}")
            return jsonify(ResponseConstants.internal_error()), 500

    @car_controller.route('/delete_damage/<damage_id>', methods=['DELETE'])
    @swag_from('swagger/delete_damage.yml')
    def delete_damage(damage_id):
        try:
            car_service.delete_damage(damage_id)
            return jsonify(ResponseConstants.ok("Damage deleted successfully")), 200
        except Exception as e:
            print(f"Error occurred while deleting damage: {e}")
            return jsonify(ResponseConstants.internal_error()), 500

    @car_controller.route('/get_all_cars', methods=['GET'])
    @swag_from('swagger/get_all_cars.yml')
    def get_all_cars():
        try:
            models = car_service.get_all_cars()
            return jsonify(ResponseConstants.ok([model.to_dict() for model in models])), 200
        except Exception as e:
            print(f"Error occurred while fetching all cars: {e}")
            return jsonify(ResponseConstants.internal_error()), 500

    @car_controller.route('/get_plate_damage', methods=['GET'])
    @swag_from('swagger/get_plate_damage.yml')
    def get_damage_by_plate():
        try:
            plate = request.args.get('plate')
            if not plate:
                return jsonify(ResponseConstants.bad_request()), 400

            car = car_service.get_damage_by_plate(plate)
            if not car:
                return jsonify(ResponseConstants.not_found()), 404

            return jsonify(ResponseConstants.ok(car.to_dict())), 200
        except Exception as e:
            print(f"Error occurred while fetching damage by plate: {e}")
            return jsonify(ResponseConstants.internal_error()), 500

    @car_controller.route('/get_report_by_damage', methods=['POST'])
    @swag_from('swagger/get_report_by_damage.yml')
    def get_report_by_damage():
        try:
            data = request.json
            part = data.get('part')
            damage_type = data.get('type')

            if not all([part, damage_type]):
                return jsonify(ResponseConstants.bad_request()), 400

            result = car_service.get_report_by_damage(part, damage_type)
            return jsonify(ResponseConstants.ok(result), 200)

        except ValueError as ve:
            print(f"Value error occurred: {ve}")
            return jsonify(ResponseConstants.bad_request()), 400

        except RuntimeError as re:
            print(f"Runtime error occurred: {re}")
            return jsonify(ResponseConstants.internal_error()), 500

    @car_controller.route('/get_damage_report_from_image', methods=['POST'])
    @swag_from('swagger/get_damage_report_from_image.yml')
    def get_damage_report_from_image():
        try:
            data = request.json
            image_base64 = data.get('image')  # The base64-encoded image

            if not image_base64:
                return jsonify(ResponseConstants.bad_request()), 400

            result = car_service.get_report_by_image(image_base64)

            if isinstance(result, str) and result.endswith('.pdf'):  # If the result is a message
                return send_file(result, as_attachment=True)
            else:  # If the result is a PDF path
                return jsonify(ResponseConstants.not_found()), 500

        except ValueError as ve:
            print(f"Value error occurred: {ve}")
            return jsonify(ResponseConstants.bad_request()), 400

        except RuntimeError as re:
            print(f"Runtime error occurred: {re}")
            return jsonify(ResponseConstants.internal_error()), 500

    return car_controller

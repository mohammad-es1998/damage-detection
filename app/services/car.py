import base64
import io
import os
import string
import tempfile

from PIL import Image

from app.ai.license_plate_pipeline import LicensePlatePipeline
from app.models.car import Car
from app.models.damage import CarDamage
from app.report.generate_poly import generate_polygons
from app.report.pdf import generate_pdf
from app.repositories.car import CarRepository
from app.repositories.damage import CarDamageRepository

class CarService:
    def __init__(self, car_repository: CarRepository, damage_repository: CarDamageRepository):
        self.pipeline = LicensePlatePipeline()
        self.car_repository = car_repository
        self.damage_repository = damage_repository

    def get_all_cars(self):
        return self.car_repository.get_all()

    def get_damage_by_plate(self, plate: string):
        return self.car_repository.get_car_with_damages(plate)

    def add_car(self, car_data):
        car = Car(**car_data)
        self.car_repository.add_car(car)

    def update_car(self, car_data):
        car = Car(**car_data)
        self.car_repository.update_car(car)

    def delete_car(self, plate):
        self.car_repository.delete_car(plate)

    def add_damage(self, damage_data):
        damage = CarDamage(**damage_data)
        self.damage_repository.add_damage(damage)

    def update_damage(self, damage_data):
        damage = CarDamage(**damage_data)
        self.damage_repository.update_damage(damage)

    def delete_damage(self, damage_id):
        self.damage_repository.delete_damage(damage_id)

    def get_report_by_image(self, image_base64):
        plate = ""
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            image = image.convert("RGB")  # Ensure the image is in RGB mode
        except Exception as e:
            raise ValueError(f"Error decoding image: {e}")

        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file_path = temp_file.name
            image.save(temp_file_path)

        try:
            # Process the image using LicensePlatePipeline
            plate = self.pipeline.process(temp_file_path)  # Assuming this method takes a file path and returns the
        except Exception as e:
            raise RuntimeError(f"Error processing image: {e}")

        pdf_path = "report.pdf"
        try:
            car = self.car_repository.get_car_with_damages(plate)
            if car:
                damages_list = [damage.part for damage in car.damages]
                path = generate_polygons(damages_list)
                generate_pdf(car, path, pdf_path)
            else:
                return "This plate is not in the database."
        except Exception as e:
            raise RuntimeError(f"Error retrieving repository: {e}")
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
        return pdf_path

    def get_report_by_damage(self, part: string, damage_type: string):
        return self.damage_repository.get_by_part_and_type(part, damage_type)

from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.car import Car


class CarRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all(self):
        try:
            return self.db_session.query(Car).all()
        except SQLAlchemyError as e:
            print(f"Error occurred while fetching all cars: {e}")
            self.db_session.rollback()
            raise

    def get_by_plate(self, car_id):
        try:
            return self.db_session.query(Car).filter_by(id=car_id).first()
        except SQLAlchemyError as e:
            print(f"Error occurred while fetching car by plate: {e}")
            self.db_session.rollback()
            raise

    def get_car_with_damages(self, plate):
        try:
            return self.db_session.query(Car).filter_by(plate=plate).options(joinedload(Car.damages)).first()
        except SQLAlchemyError as e:
            print(f"Error occurred while fetching car with damages: {e}")
            self.db_session.rollback()
            raise

    def add_car(self, car):
        try:
            self.db_session.add(car)
            self.db_session.commit()
        except SQLAlchemyError as e:
            print(f"Error occurred while adding car: {e}")
            self.db_session.rollback()
            raise

    def delete_car(self, car_plate):
        try:
            car = self.db_session.query(Car).filter_by(plate=car_plate).first()
            if car:
                self.db_session.delete(car)
                self.db_session.commit()
            else:
                print("Car not found")
        except SQLAlchemyError as e:
            print(f"Error occurred while deleting car: {e}")
            self.db_session.rollback()
            raise

    def update_car(self, car):
        try:
            existing_car = self.db_session.query(Car).filter_by(plate=car.plate).first()
            if existing_car:
                existing_car.model = car.model
                existing_car.color = car.color
                existing_car.vin = car.vin
                existing_car.brand = car.brand
                self.db_session.commit()
            else:
                print("Car not found")
        except SQLAlchemyError as e:
            print(f"Error occurred while updating car: {e}")
            self.db_session.rollback()
            raise

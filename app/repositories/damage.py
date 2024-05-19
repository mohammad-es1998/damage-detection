from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models.car import Car
from app.models.damage import CarDamage


class CarDamageRepository:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_all(self):
        try:
            return self.db_session.query(CarDamage).all()
        except SQLAlchemyError as e:
            print(f"Error occurred while fetching all CarDamage: {e}")
            self.db_session.rollback()
            raise

    def get_by_part_and_type(self, part, damage_type):
        try:
            car_damages = self.db_session.query(CarDamage).filter(
                CarDamage.part == part, CarDamage.damage_type == damage_type
            ).all()
            # Convert CarDamage objects to dictionaries
            return [damage.to_dict() for damage in car_damages]
        except SQLAlchemyError as e:
            print(f"Error occurred while fetching CarDamage by part and type: {e}")
            self.db_session.rollback()
            raise

    def add_damage(self, damage):
        try:
            self.db_session.add(damage)
            self.db_session.commit()
        except SQLAlchemyError as e:
            print(f"Error occurred while adding damage: {e}")
            self.db_session.rollback()
            raise

    def delete_damage(self, damage_id):
        try:
            damage = self.db_session.query(CarDamage).filter_by(id=damage_id).first()
            if damage:
                self.db_session.delete(damage)
                self.db_session.commit()
            else:
                print("Damage not found")
        except SQLAlchemyError as e:
            print(f"Error occurred while deleting damage: {e}")
            self.db_session.rollback()
            raise

    def update_damage(self, damage):
        try:
            existing_damage = self.db_session.query(CarDamage).filter_by(id=damage.id).first()
            if existing_damage:
                existing_damage.plate = damage.plate
                existing_damage.damage_type = damage.damage_type
                existing_damage.part = damage.part
                self.db_session.commit()
            else:
                print("Damage not found")
        except SQLAlchemyError as e:
            print(f"Error occurred while updating damage: {e}")
            self.db_session.rollback()
            raise


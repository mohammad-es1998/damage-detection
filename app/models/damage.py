from sqlalchemy import Column, String, INT, ForeignKey

from app.database.database import Base


class CarDamage(Base):
    __tablename__ = 'car_damages'
    id = Column(INT,primary_key=True,autoincrement=True)
    plate = Column(String, ForeignKey('car.plate'))
    damage_type = Column(String)
    part = Column(String)

    def to_dict(self):
        return {
            'plate': self.plate,
            'damage_type': self.damage_type,
            'part': self.part,
        }


# car = relationship('Car', back_populates='car_damages')

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Car(Base):
    __tablename__ = 'car'
    plate = Column(String, primary_key=True)
    model = Column(String)
    color = Column(String)
    vin = Column(String)
    brand = Column(String)
    damages = relationship('CarDamage', backref='car', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'plate': self.plate,
            'model': self.model,
            'color': self.color,
            'vin': self.vin,
            'brand': self.brand,
            'damages': [damage.to_dict() for damage in self.damages]
        }

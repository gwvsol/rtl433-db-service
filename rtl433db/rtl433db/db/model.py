from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey


class CommonBase(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=CommonBase)


class Sensors(Base):

    model = Column(String, nullable=False, index=True)
    sensor_id = Column(String, nullable=False)
    datetime = Column(DateTime(timezone=True),
                      default=datetime.now())


class Temperature(Base):

    sensor_id = Column(Integer,
                       ForeignKey("sensors.id"),
                       nullable=False, index=True)
    sensor_model = relationship("Sensors",
                                lazy="joined")
    temperature = Column(Float, nullable=False)
    datetime = Column(DateTime(timezone=True),
                      default=datetime.now())

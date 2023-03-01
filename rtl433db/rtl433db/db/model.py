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
    humidity = Column(Integer)
    datetime = Column(DateTime(timezone=True),
                      default=datetime.now())


class WeatherLocation(Base):

    location = Column(String, nullable=False, index=True)
    country = Column(String, nullable=False, index=True)
    lat = Column(Float)
    lon = Column(Float)
    datetime = Column(DateTime(timezone=True),
                      default=datetime.now())


class Weather(Base):

    location = Column(Integer,
                      ForeignKey("weatherlocation.id"),
                      nullable=False, index=True)
    # Температура (в градусах Цельсия)
    temp_c = Column(Float, nullable=False)
    # Температура по ощущениям (в градусах Цельсия)
    temp_feelslike_c = Column(Float)
    # Скорость ветра в км/час
    wind_kph = Column(Float)
    # Направление ветра в градусах
    wind_degree = Column(Integer)
    # Направление ветра в виде компаса с 16 точками
    wind_dir = Column(String)
    # Давление в миллибарах (mmHg value = mbar value x 0.750062)
    pressure_mb = Column(Float)
    # Давление в мм ртутного столба
    pressure_mmhg = Column(Float)
    # Количество осадков в мм
    precip_mm = Column(Integer)
    # Влажность в %
    humidity = Column(Integer)
    # Порывы ветра в км/час
    gust_kph = Column(Float)
    datetime = Column(DateTime(timezone=True),
                      default=datetime.now())

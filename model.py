from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import declarative_base


engine = create_engine("sqlite:///vehicles.db")
Base = declarative_base()

class Vehicle(Base):

    __tablename__ = 'vehicle'
    id = Column(Integer, primary_key=True)
    brand = Column(String(30), nullable=False)
    name = Column(String(50), nullable=False)
    year = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)
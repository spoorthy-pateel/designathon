from sqlalchemy import Column, Integer, String, Float, Enum
from base import Base
import enum

class TrainingLevel(enum.Enum):
    beginner = "Beginner"
    intermediate = "Intermediate"
    advanced = "Advanced"

class Training(Base):
    __tablename__ = 'trainings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    training_name = Column(String, nullable=False)
    technologies_learnt = Column(String, nullable=False)
    level_of_training = Column(Enum(TrainingLevel), nullable=False)
    duration = Column(Float, nullable=False)

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class ConsultantTraining(Base):
    __tablename__ = 'consultant_trainings'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    training_id = Column(Integer, ForeignKey('trainings.id'), nullable=False)
    attended_hours = Column(Float, nullable=False)
    
    # Relationships
    consultant = relationship("Consultant", back_populates="consultant_trainings")
    training = relationship("Training")

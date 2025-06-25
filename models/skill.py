from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Skill(Base):
    __tablename__ = 'skills'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    technologies_known = Column(String, nullable=False)
    years_of_experience = Column(Float, nullable=False)
    strength_of_skill = Column(Integer, nullable=False)
    consultant = relationship("Consultant", back_populates="skills")

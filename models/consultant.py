from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from base import Base

class Consultant(Base):
    __tablename__ = 'consultants'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    emp_id = Column(String, unique=True, nullable=False)
    mobile_no = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=True)
    current_role = Column(String, nullable=True)
    skills = relationship("Skill", back_populates="consultant")
    certifications = relationship("Certification", back_populates="consultant")
    professional_details = relationship("Professional", back_populates="consultant", uselist=False)
    consultant_opportunities = relationship("ConsultantOpportunity", back_populates="consultant")
    consultant_trainings = relationship("ConsultantTraining", back_populates="consultant")

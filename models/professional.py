from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Professional(Base):
    __tablename__ = 'professionals'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    last_worked_organization = Column(String, nullable=False)
    recent_role = Column(String, nullable=False)
    recent_project = Column(String, nullable=True)
    recent_start_date = Column(Date, nullable=True)
    recent_project_release_date = Column(Date, nullable=True)
    
    # Relationship
    consultant = relationship("Consultant", back_populates="professional_details")

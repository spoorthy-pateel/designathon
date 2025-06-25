from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from base import Base

class Certification(Base):
    __tablename__ = 'certifications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    certification_name = Column(String, nullable=False)
    issued_date = Column(Date, nullable=False)
    valid_till = Column(Date, nullable=True)
    
    # Relationship
    consultant = relationship("Consultant", back_populates="certifications")

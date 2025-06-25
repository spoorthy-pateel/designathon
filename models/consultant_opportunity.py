from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from base import Base
import enum

class SelectionStatus(enum.Enum):
    selected = "Selected"
    rejected = "Rejected"
    pending = "Pending"

class ConsultantOpportunity(Base):
    __tablename__ = 'consultant_opportunities'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    consultant_id = Column(Integer, ForeignKey('consultants.id'), nullable=False)
    opportunity_id = Column(Integer, ForeignKey('opportunities.id'), nullable=False)
    selection_status = Column(Enum(SelectionStatus), nullable=False)
    remarks = Column(String, nullable=True)
    
    # Relationships
    consultant = relationship("Consultant", back_populates="consultant_opportunities")
    opportunity = relationship("Opportunity")

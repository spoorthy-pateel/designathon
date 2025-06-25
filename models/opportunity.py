from sqlalchemy import Column, Integer, String, Float, Date
from base import Base

class Opportunity(Base):
    __tablename__ = 'opportunities'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    skills_expected = Column(String, nullable=False)
    years_of_experience_required = Column(Float, nullable=False)
    deadline = Column(Date, nullable=False)

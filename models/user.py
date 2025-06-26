from sqlalchemy import Column, Integer, String, Date,Enum
from sqlalchemy.orm import relationship
from base import Base
import enum

class Role(enum.Enum):
    Admin = "Admin"
    Consultant= "Consultant"

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    emp_id = Column(Integer,unique=True, nullable=False)
    password=Column(String,nullable=False)
    role=Column(Enum(Role), nullable=False)
    consultant = relationship("Consultant", back_populates="user", uselist=False)

    
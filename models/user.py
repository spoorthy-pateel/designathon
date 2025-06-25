from sqlalchemy import Column, Integer, String, Date,Enum
from sqlalchemy.orm import relationship
from base import Base
import enum

class Role(enum.Enum):
    Admin = "Admin"
    Consultant= "Consultant"

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    password=Column(String,nullable=False)
    role=Column(Enum(Role), nullable=False)

    
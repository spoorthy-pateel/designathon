from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base  # Import Base from base.py
 
from models.consultant import Consultant
from models.skill import Skill
from models.certification import Certification
from models.professional import Professional
from models.opportunity import Opportunity
from models.consultant_opportunity import ConsultantOpportunity
from models.training import Training
from models.consultant_training import ConsultantTraining
from models.user import User
 
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/designathon"
 
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
 
def init_db():
    print("Creating tables...")
    print(Base.metadata.tables)  # Debugging line
    Base.metadata.create_all(bind=engine)
    print("Tables created!")
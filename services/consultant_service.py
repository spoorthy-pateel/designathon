from sqlalchemy.orm import Session
from models.consultant import Consultant
from models.user import User

class ConsultantService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_consultant(self, name: str, emp_id: str, mobile_no: str, email: str, address: str = None, current_role: str = None):
        # Create a new user instance

        user = self.db_session.query(User).filter(User.emp_id == emp_id).first()
        if not user:
            return None, "User  with the given emp_id does not exist"

        existing_consultant = self.db_session.query(Consultant).filter(
            (Consultant.emp_id == emp_id) | (Consultant.email == email)
        ).first()

        if existing_consultant:
            return None,"Employee with the same Id or Email Address already exists"
        
        new_consultant = Consultant(name=name,emp_id=emp_id,mobile_no=mobile_no,email=email,address=address,current_role=current_role,user_id=user.user_id)
        
        # Add and commit the user to the database
        self.db_session.add(new_consultant)
        self.db_session.commit()
        
        return new_consultant,None
    
    def get_consultant(self , consultant_id:int):
        consultant = self.db_session.query(Consultant).filter(Consultant.id==consultant_id).first()
        if not consultant:
            return None, "No consultant found with the id"+consultant_id
        return consultant,None
    
    def get_all_consultants(self):
        consultants = self.db_session.query(Consultant).all()
        return consultants
    
    def update_consultant(self,consultant_id:int,**kwargs):
        consultant = self.db_session.query(Consultant).filter(Consultant.id==consultant_id).first()
        if not consultant:
            return None, "No consultant found with the id"+consultant_id
        
        kwargs.pop('user_id', None)

        for key, value in kwargs.items():
            if hasattr(consultant, key):
                setattr(consultant, key, value)

        # Commit the changes to the database
        self.db_session.commit()
        return consultant, None
    
    def delete_consultant(self,consultant_id:int):
        consultant = self.db_session.query(Consultant).filter(Consultant.id==consultant_id).first()
        if not consultant:
            return None, "No consultant found with the id"+consultant_id
        self.db_session.delete(consultant)
        self.db_session.commit()
        return True,None
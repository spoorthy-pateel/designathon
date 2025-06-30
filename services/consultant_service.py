from sqlalchemy.orm import Session
from models.consultant import Consultant
from models.user import User
import traceback

class ConsultantService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_consultant(self, name: str, emp_id: str, mobile_no: str, email: str, address: str = None, current_role: str = None, user_id: int = None):
        try:
            if not user_id:
                return None, "user_id is required"

            user = self.db_session.query(User).filter(User.user_id == user_id).first()
            if not user:
                return None, "User with the given user_id does not exist"

            existing_consultant = self.db_session.query(Consultant).filter(
                (Consultant.emp_id == emp_id) | (Consultant.email == email)
            ).first()

            if existing_consultant:
                return None, "Employee with the same Id or Email Address already exists"

            new_consultant = Consultant(
                name=name,
                emp_id=emp_id,
                mobile_no=mobile_no,
                email=email,
                address=address,
                current_role=current_role,
                user_id=user_id  # Use user_id directly
            )
            self.db_session.add(new_consultant)
            self.db_session.commit()
            return new_consultant, None
        except Exception as e:
            traceback.print_exc()
            return None, str(e)
    
    def get_consultant(self , consultant_id:int):
        try:
            consultant = self.db_session.query(Consultant).filter(Consultant.id==consultant_id).first()
            if not consultant:
                return None, f"No consultant found with the id {consultant_id}"
            return consultant, None
        except Exception as e:
            traceback.print_exc()
            return None, str(e)
    
    def get_all_consultants(self):
        try:
            consultants = self.db_session.query(Consultant).all()
            return consultants
        except Exception as e:
            traceback.print_exc()
            return []
    
    def update_consultant(self,consultant_id:int,**kwargs):
        try:
            consultant = self.db_session.query(Consultant).filter(Consultant.id==consultant_id).first()
            if not consultant:
                return None, f"No consultant found with the id {consultant_id}"
            
            kwargs.pop('user_id', None)

            for key, value in kwargs.items():
                if hasattr(consultant, key):
                    setattr(consultant, key, value)

            # Commit the changes to the database
            self.db_session.commit()
            return consultant, None
        except Exception as e:
            traceback.print_exc()
            return None, str(e)
    
    def delete_consultant(self,consultant_id:int):
        try:
            consultant = self.db_session.query(Consultant).filter(Consultant.id==consultant_id).first()
            if not consultant:
                return None, f"No consultant found with the id {consultant_id}"
            self.db_session.delete(consultant)
            self.db_session.commit()
            return True, None
        except Exception as e:
            traceback.print_exc()
            return None, str(e)
    
    def get_consultant_by_emp_id(self, emp_id: str):
        """
        Fetch a consultant by their employee ID.
        Returns the Consultant object if found, else None.
        """
        try:
            return self.db_session.query(Consultant).filter(Consultant.emp_id == emp_id).first()
        except Exception as e:
            traceback.print_exc()
            return None
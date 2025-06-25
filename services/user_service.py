from sqlalchemy.orm import Session
from models.user import User, Role

class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_user(self, user_name: str, password: str, role: Role):
        # Create a new user instance
        new_user = User(user_name=user_name, password=password, role=role)
        
        # Add and commit the user to the database
        self.db_session.add(new_user)
        self.db_session.commit()
        
        return new_user

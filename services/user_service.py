from sqlalchemy.orm import Session
from models.user import User, Role
from werkzeug.security import generate_password_hash ,check_password_hash

class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_user(self, user_name: str, password: str, role: Role):
        # Create a new user instance
        new_user = User(user_name=user_name, password=generate_password_hash(password), role=role)
        
        # Add and commit the user to the database
        self.db_session.add(new_user)
        self.db_session.commit()
        
        return new_user

    def validate_user(self , user_name:str , password: str):
        user = self.db_session.query(User).filter(User.user_name==user_name).first()
        if not user:
            return None,"Invalid user name or password"
        if not check_password_hash(user.password,password):
            return None,"Invalid user name or password"
        return user,None
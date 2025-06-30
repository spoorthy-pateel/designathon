from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User, Role
from werkzeug.security import generate_password_hash, check_password_hash

class UserService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_user(self, emp_id: int, password: str, role: Role):
        # Check if user already exists
        existing_user = self.db_session.query(User).filter(User.emp_id == emp_id).first()
        if existing_user:
            raise ValueError("A user with this Employee ID already exists.")

        # Create a new user instance
        new_user = User(emp_id=emp_id, password=generate_password_hash(password), role=role)
        self.db_session.add(new_user)
        try:
            self.db_session.commit()
        except IntegrityError as e:
            self.db_session.rollback()
            raise ValueError("A user with this Employee ID already exists.")
        except Exception as e:
            self.db_session.rollback()
            raise e

        return new_user

    def validate_user(self, emp_id: int, password: str):
        user = self.db_session.query(User).filter(User.emp_id == emp_id).first()
        if not user:
            return None, "Invalid employee id or password"
        if not check_password_hash(user.password, password):
            return None, "Invalid employee id or password"
        return user, None

    def get_user_by_emp_id(self, emp_id: int):
        """
        Fetch a user by their employee ID.
        Returns the User object if found, else None.
        """
        return self.db_session.query(User).filter(User.emp_id == emp_id).first()
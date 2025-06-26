from sqlalchemy.orm import Session
from models.consultant_training import ConsultantTraining

class ConsultantTrainingService:
    def __init__(self, db_session):
        self.db_session = db_session



    def add_consultant_training(self, consultant_id: int, training_id: int, attended_hours: float):
        # Create a new ConsultantTraining instance
        new_consultant_training = ConsultantTraining(
            consultant_id=consultant_id,
            training_id=training_id,
            attended_hours=attended_hours
        )
        print("The service is starting...")
        # Add and commit the consultant training to the database
        self.db_session.add(new_consultant_training)
        self.db_session.commit()

        return new_consultant_training

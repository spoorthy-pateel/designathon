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

    def update_consultant_training(self, id: int, consultant_id: int, training_id: int, attended_hours: float):
    # Fetch the existing ConsultantTraining instance
        consultant_training = self.db_session.query(ConsultantTraining).filter_by(id=id).first()

        if not consultant_training:
            return None  # Return None if the record is not found

        # Update the fields
        consultant_training.consultant_id = consultant_id
        consultant_training.training_id = training_id
        consultant_training.attended_hours = attended_hours

        # Commit the changes to the database
        self.db_session.commit()

        return consultant_training


    def get_consultant_training_by_id(self, id: int):
        # Fetch the ConsultantTraining instance by ID
        consultant_training = self.db_session.query(ConsultantTraining).filter_by(id=id).first()

        return consultant_training  # Return the instance or None if not found


    def delete_consultant_training_by_id(self, id: int):
    # Fetch the ConsultantTraining instance by ID
        consultant_training = self.db_session.query(ConsultantTraining).filter_by(id=id).first()

        if not consultant_training:
            return False  # Return False if the record is not found

        # Delete the record
        self.db_session.delete(consultant_training)
        self.db_session.commit()

        return True  # Return True if deletion is successful


    def get_all_consultant_trainings(self):
    # Fetch all ConsultantTraining entries from the database
        consultant_trainings = self.db_session.query(ConsultantTraining).all()

        return consultant_trainings  # Return the list of all entries


    def get_consultant_trainings_by_consultant_id(self, consultant_id: int):
    # Fetch all ConsultantTraining entries for the given consultant_id
        consultant_trainings = self.db_session.query(ConsultantTraining).filter_by(consultant_id=consultant_id).all()

        return consultant_trainings  # Return the list of entries or an empty list if none are found


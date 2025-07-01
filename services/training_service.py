from sqlalchemy.orm import Session
from models.training import Training, TrainingLevel

class TrainingService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_training(self, training_name: str, technologies_learnt: str, level_of_training: TrainingLevel, duration: float):
        new_training = Training(
            training_name=training_name,
            technologies_learnt=technologies_learnt,
            level_of_training=level_of_training,
            duration=duration
        )
        self.db_session.add(new_training)
        self.db_session.commit()
        return new_training

    def update_training(self, training_id: int, training_name: str = None, technologies_learnt: str = None, level_of_training: TrainingLevel = None, duration: float = None):
        training = self.db_session.query(Training).filter(Training.id == training_id).first()
        if not training:
            return None
        if training_name:
            training.training_name = training_name
        if technologies_learnt:
            training.technologies_learnt = technologies_learnt
        if level_of_training:
            training.level_of_training = level_of_training
        if duration:
            training.duration = duration
        self.db_session.commit()
        return training

    def get_training_by_id(self, training_id: int):
        return self.db_session.query(Training).filter(Training.id == training_id).first()

    def delete_training_by_id(self, training_id: int):
        training = self.db_session.query(Training).filter(Training.id == training_id).first()
        if not training:
            return None
        self.db_session.delete(training)
        self.db_session.commit()
        return training

    def get_all_trainings(self):
        return self.db_session.query(Training).all()

    def get_trainings_by_ids(self, training_ids):
        """
        Fetch multiple trainings by a list of IDs.
        """
        return (
            self.db_session.query(Training)
            .filter(Training.id.in_(training_ids))
            .all()
        )
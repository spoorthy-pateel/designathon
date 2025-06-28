from sqlalchemy.orm import Session
from models.skill import Skill

class SkillsService:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def add_skill(self, consultant_id: int, technologies_known: str, years_of_experience: float, strength_of_skill: int):
        new_skill = Skill(
            consultant_id=consultant_id,
            technologies_known=technologies_known,
            years_of_experience=years_of_experience,
            strength_of_skill=strength_of_skill
        )
        self.db_session.add(new_skill)
        self.db_session.commit()
        return new_skill

    def get_skill(self, skill_id: int):
        return self.db_session.query(Skill).filter(Skill.id == skill_id).first()

    def get_skills_by_consultant(self, consultant_id: int):
        return self.db_session.query(Skill).filter(Skill.consultant_id == consultant_id).all()

    def get_all_skills(self):
        return self.db_session.query(Skill).all()

    def update_skill(self, skill_id: int, **kwargs):
        skill = self.db_session.query(Skill).filter(Skill.id == skill_id).first()
        if not skill:
            return None
        for key, value in kwargs.items():
            if hasattr(skill, key):
                setattr(skill, key, value)
        self.db_session.commit()
        return skill

    def delete_skill(self, skill_id: int):
        skill = self.db_session.query(Skill).filter(Skill.id == skill_id).first()
        if not skill:
            return False
        self.db_session.delete(skill)
        self.db_session.commit()
        return True

    def get_skills_by_emp_id(self, emp_id: str):
        """
        Fetch all skills for a consultant using their employee ID.
        Returns a list of Skill objects or an empty list if none found.
        """
        from models.consultant import Consultant
        consultant = self.db_session.query(Consultant).filter(Consultant.emp_id == emp_id).first()
        if not consultant:
            return []
        return self.db_session.query(Skill).filter(Skill.consultant_id == consultant.id).all()

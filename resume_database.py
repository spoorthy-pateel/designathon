from sqlalchemy.orm import Session
from models.skill import Skill
from models.certification import Certification
from models.professional import Professional

def insert_resume_data(data, user_id, db_session: Session):
    # Insert skills
    for skill in data.get('skills', []):
        db_skill = Skill(
            user_id=user_id,
            technologies_known=skill.get('technologies_known'),
            years_of_experience=skill.get('years_of_experience'),
            strength_of_skill=skill.get('strength_of_skill')
        )
        db_session.add(db_skill)

    # Insert certifications
    for cert in data.get('certifications', []):
        db_cert = Certification(
            user_id=user_id,
            certification_name=cert.get('certification_name'),
            issued_date=cert.get('issued_date'),
            valid_till=cert.get('valid_till')
        )
        db_session.add(db_cert)

    # Insert professional info (assuming one per resume)
    prof = data.get('professional', {})
    if prof:
        db_prof = Professional(
            user_id=user_id,
            last_worked_organization=prof.get('last_worked_organization'),
            recent_role=prof.get('recent_role'),
            recent_project=prof.get('recent_project'),
            recent_start_date=prof.get('recent_start_date'),
            recent_project_release_date=prof.get('recent_project_release_date')
        )
        db_session.add(db_prof)

    db_session.commit()
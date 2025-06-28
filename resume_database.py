from sqlalchemy.orm import Session
from models.skill import Skill
from models.certification import Certification
from models.professional import Professional
from models.consultant import Consultant

def insert_resume_data(data, emp_id: str, db_session: Session):
    # Get consultant_id from emp_id
    consultant = db_session.query(Consultant).filter(Consultant.emp_id == emp_id).first()
    if not consultant:
        raise ValueError(f"No consultant found with emp_id {emp_id}")
    consultant_id = consultant.id

    # Insert skills
    for skill in data.get('skills', []):
        db_skill = Skill(
            consultant_id=consultant_id,
            technologies_known=skill.get('technologies_known') or 'Unknown',
            years_of_experience=skill.get('years_of_experience') or 0.0,
            strength_of_skill=skill.get('strength_of_skill') or 1
        )
        db_session.add(db_skill)

    # Insert certifications
    for cert in data.get('certifications', []):
        db_cert = Certification(
            consultant_id=consultant_id,
            certification_name=cert.get('certification_name') or 'Unknown',
            issued_date=cert.get('issued_date') or '1970-01-01',
            valid_till=cert.get('valid_till')  # null allowed
        )
        db_session.add(db_cert)

    # Insert professional info (assuming one per resume)
    prof = data.get('professional', {})
    if prof:
        db_prof = Professional(
            consultant_id=consultant_id,
            last_worked_organization=prof.get('last_worked_organization') or 'Unknown',
            recent_role=prof.get('recent_role') or 'Unknown',
            recent_project=prof.get('recent_project'),  # null allowed
            recent_start_date=prof.get('recent_start_date') or '1970-01-01',
            recent_project_release_date=prof.get('recent_project_release_date')  # null allowed
        )
        db_session.add(db_prof)

    db_session.commit()

from database import SessionLocal
from models.consultant_opportunity import ConsultantOpportunity, SelectionStatus

def create_consultant_opportunity(consultant_id, opportunity_id, selection_status=SelectionStatus.pending, remarks=None):
    db = SessionLocal()
    try:
        co = ConsultantOpportunity(
            consultant_id=consultant_id,
            opportunity_id=opportunity_id,
            selection_status=selection_status,
            remarks=remarks
        )
        db.add(co)
        db.commit()
        db.refresh(co)
        return co
    finally:
        db.close()

def get_consultant_opportunities_by_consultant(consultant_id):
    db = SessionLocal()
    try:
        return db.query(ConsultantOpportunity).filter_by(consultant_id=consultant_id).all()
    finally:
        db.close()

def update_selection_status(co_id, status, remarks=None):
    db = SessionLocal()
    try:
        co = db.query(ConsultantOpportunity).filter_by(id=co_id).first()
        if not co:
            return None
        co.selection_status = status
        if remarks is not None:
            co.remarks = remarks
        db.commit()
        db.refresh(co)
        return co
    finally:
        db.close()

def get_by_id(co_id):
    db = SessionLocal()
    try:
        return db.query(ConsultantOpportunity).filter_by(id=co_id).first()
    finally:
        db.close()
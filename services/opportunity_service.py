from models.opportunity import Opportunity

class OpportunityService:
    def __init__(self, db_session):
        self.db_session = db_session

    def get_opportunity_by_id(self, opportunity_id):
        return self.db_session.query(Opportunity).filter_by(id=opportunity_id).first()

    def get_opportunities_by_ids(self, ids):
        return self.db_session.query(Opportunity).filter(Opportunity.id.in_(ids)).all()

    def get_all_opportunities(self):
        return self.db_session.query(Opportunity).all()
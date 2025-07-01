from sqlalchemy.orm import Session
from models.opportunity import Opportunity
from datetime import datetime

class OpportunityService:
    def __init__(self, db_session):
            self.db_session = db_session



    def create_opportunity(self, name: str, skills_expected: str, years_of_experience_required: float, deadline: str):
    # Create a new Opportunity instance
        print(datetime.now())
        new_opportunity = Opportunity(
            name=name,
            skills_expected=skills_expected,
            years_of_experience_required=years_of_experience_required,
            deadline=datetime.strptime(deadline, '%Y-%m-%d')
        )

        # Add to the database and commit
        self.db_session.add(new_opportunity)
        self.db_session.commit()

        return new_opportunity  # Return the newly created opportunity

    
    def get_opportunity_by_id(self, id: int):
        # Fetch the Opportunity instance by ID
        opportunity = self.db_session.query(Opportunity).filter_by(id=id).first()

        return opportunity  # Return the opportunity or None if not found

    
    def update_opportunity(self, id: int, name: str = None, skills_expected: str = None, years_of_experience_required: float = None, deadline: str = None):
        # Fetch the Opportunity instance by ID
        opportunity = self.db_session.query(Opportunity).filter_by(id=id).first()

        if not opportunity:
            return None  # Return None if the record is not found

        # Update the fields if provided
        if name:
            opportunity.name = name
        if skills_expected:
            opportunity.skills_expected = skills_expected
        if years_of_experience_required:
            opportunity.years_of_experience_required = years_of_experience_required
        if deadline:
            opportunity.deadline = datetime.strptime(deadline, '%Y-%m-%d')

        # Commit the changes
        self.db_session.commit()

        return opportunity  # Return the updated opportunity

    def delete_opportunity_by_id(self, id: int):
        # Fetch the Opportunity instance by ID
        opportunity = self.db_session.query(Opportunity).filter_by(id=id).first()

        if not opportunity:
            return False  # Return False if the record is not found

        # Delete the record
        self.db_session.delete(opportunity)
        self.db_session.commit()

        return True  # Return True if deletion is successful

    def get_all_opportunities(self):
        # Fetch all Opportunity entries from the database
        opportunities = self.db_session.query(Opportunity).all()

        return opportunities  # Return the list of all opportunities or an empty list if none are found

    def get_opportunities_by_ids(self, ids):
       return self.db_session.query(Opportunity).filter(Opportunity.id.in_(ids)).all()






# class OpportunityService:
#     def __init__(self, db_session):
#         self.db_session = db_session

#     def get_opportunity_by_id(self, opportunity_id):
#         return self.db_session.query(Opportunity).filter_by(id=opportunity_id).first()

#     def get_opportunities_by_ids(self, ids):
#         return self.db_session.query(Opportunity).filter(Opportunity.id.in_(ids)).all()

#     def get_all_opportunities(self):
#         return self.db_session.query(Opportunity).all()

from sqlalchemy.orm import Session
from models.consultant_opportunity import ConsultantOpportunity,SelectionStatus

class ConsultantOpportunityService:
    def __init__(self, db_session):
        self.db_session = db_session

    def add_consultant_opportunity(self, consultant_id: int, opportunity_id: int, selection_status: str, remarks: str):
        try:
            # Create a new ConsultantOpportunity instance
            new_consultant_opportunity = ConsultantOpportunity(
                consultant_id=consultant_id,
                opportunity_id=opportunity_id,
                selection_status=SelectionStatus(selection_status),
                remarks=remarks
            )

            # Add and commit the consultant opportunity to the database
            self.db_session.add(new_consultant_opportunity)
            self.db_session.commit()

            return new_consultant_opportunity
        except Exception as e:
            raise Exception(f"Error adding consultant opportunity: {str(e)}") 


    def get_consultant_opportunity_by_id(self, id: int):
        # Fetch the ConsultantOpportunity instance by ID
        consultant_opportunity = self.db_session.query(ConsultantOpportunity).filter_by(id=id).first()

        return consultant_opportunity  # Return the consultant opportunity or None if not found

    def update_consultant_opportunity(self, id: int, consultant_id: int = None, opportunity_id: int = None, selection_status: str = None, remarks: str = None):
        # Fetch the ConsultantOpportunity instance by ID
        consultant_opportunity = self.db_session.query(ConsultantOpportunity).filter_by(id=id).first()

        if not consultant_opportunity:
            return None  # Return None if the record is not found

        # Update the fields if provided
        if consultant_id:
            consultant_opportunity.consultant_id = consultant_id
        if opportunity_id:
            consultant_opportunity.opportunity_id = opportunity_id
        if selection_status:
            consultant_opportunity.selection_status = SelectionStatus(selection_status)
        if remarks:
            consultant_opportunity.remarks = remarks

        # Commit the changes
        self.db_session.commit()

        return consultant_opportunity  # Return the updated consultant opportunity

    
    def delete_consultant_opportunity_by_id(self, id: int):
        # Fetch the ConsultantOpportunity instance by ID
        consultant_opportunity = self.db_session.query(ConsultantOpportunity).filter_by(id=id).first()

        if not consultant_opportunity:
            return False  # Return False if the record is not found

        # Delete the record
        self.db_session.delete(consultant_opportunity)
        self.db_session.commit()

        return True  # Return True if deletion is successful


    def get_all_consultant_opportunities(self):
        # Fetch all ConsultantOpportunity entries from the database
        consultant_opportunities = self.db_session.query(ConsultantOpportunity).all()

        return consultant_opportunities  # Return the list of all consultant opportunities or an empty list if none are found





            








from court_proceedings_management_application.interfaces.case_proceeding_database import CaseProceedingDatabase
from court_proceedings_management_application.interfaces.case_proceeding_interface import CaseProceedingInterface


class CaseProceedingService(CaseProceedingInterface):
    def __init__(self):
        self.case_proceeding_database = CaseProceedingDatabase()

    def get_case_proceeding_by_id(self, case_proceeding_id):
        return self.case_proceeding_database.get_case_proceeding_by_id(case_proceeding_id)

    def create_case_proceeding(self, case_id, **kwargs):
        return self.case_proceeding_database.create_case_proceeding(case_id, **kwargs)

    def update_case_proceeding(self, case_proceeding_id, **kwargs):
        return self.case_proceeding_database.update_case_proceeding(case_proceeding_id, **kwargs)

    def delete_case_proceeding(self, case_proceeding_id):
        return self.case_proceeding_database.delete_case_proceeding(case_proceeding_id)

    # case proceeding permission methods
    def grant_case_proceeding_edit_permission(self, case_proceeding, user):
        return self.case_proceeding_database.grant_case_proceeding_edit_permission(case_proceeding, user)

    # case proceeding retrieval methods
    def get_case_proceedings(self, case_id):
        return self.case_proceeding_database.get_case_proceedings(case_id)

    def get_case_proceeding_by_date(self, case_id, date):
        return self.case_proceeding_database.get_case_proceeding_by_date(case_id, date)

    def get_case_proceeding_by_case(self, case_id):
        return self.case_proceeding_database.get_case_proceeding_by_case(case_id)

    def get_document_types(self):
        return self.case_proceeding_database.get_document_types()

    def get_document_types_for_role(self, role):
        return self.case_proceeding_database.get_document_types_for_role(role)

    def get_document_confidentiality(self):
        return self.case_proceeding_database.get_document_confidentiality()

    def get_verdicts(self):
        return self.case_proceeding_database.get_verdicts()

    # relief handling methods
    def create_relief(self, participant, case_proceeding, court, relief_type, verdict, value):
        return self.case_proceeding_database.create_relief(participant, case_proceeding, court, relief_type, verdict, value)

    def get_relief_types(self):
        return self.case_proceeding_database.get_relief_types()

    def get_relief_by_id(self, relief_id):
        return self.case_proceeding_database.get_relief_by_id(relief_id)

    def get_relief_by_case_proceeding(self, case_proceeding_id):
        return self.case_proceeding_database.get_relief_by_case_proceeding(case_proceeding_id)

    def get_relief_by_participant(self, participant, case_proceeding):
        return self.case_proceeding_database.get_relief_by_participant(participant, case_proceeding)

    def update_relief(self, relief_id, participant=None, case_proceeding=None, court=None, relief_type=None, verdict=None, value=None):
        return self.case_proceeding_database.update_relief(relief_id, participant, case_proceeding, court, relief_type, verdict, value)

    def delete_relief(self, relief_id):
        return self.case_proceeding_database.delete_relief(relief_id)

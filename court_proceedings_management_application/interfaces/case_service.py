
from court_proceedings_management_application.interfaces.case_database import CaseDatabase, CaseDoesNotExist
from court_proceedings_management_application.interfaces.case_interface import CaseInterface


class CaseService(CaseInterface):
    def __init__(self):
        self.case_database = CaseDatabase()

    # Case creation methods
    def create_case(self, **kwargs):
        return self.case_database.create_case(**kwargs)

    # Case retrieval methods
    def get_case_by_id(self, case_id):
        try:
            return self.case_database.get_case_by_id(case_id)
        except CaseDoesNotExist as e:
            print(e)
            return None

    def get_all_cases(self):
        return self.case_database.get_all_cases()

    def get_case_by_name(self, name):
        return self.case_database.get_case_by_name(name)

    # Case attribute methods
    def case_types(self):
        return self.case_database.case_types()

    def case_location(self):
        return self.case_database.case_location()

    # Case modification methods
    def delete_case(self, case):
        self.case_database.delete_case(case)

    def assign_user_to_case(self, case, user, role):
        self.case_database.assign_user_to_case(case, user, role)

    def get_decision(self):
        return self.case_database.get_decision()
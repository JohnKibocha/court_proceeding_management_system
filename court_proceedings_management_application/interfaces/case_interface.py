
from abc import ABC, abstractmethod


class CaseInterface(ABC):
    # Case creation methods
    @abstractmethod
    def create_case(self, **kwargs):
        pass

    # Case retrieval methods
    @abstractmethod
    def get_case_by_id(self, case_id):
        pass

    @abstractmethod
    def get_all_cases(self):
        pass

    @abstractmethod
    def get_case_by_name(self, name):
        pass

    # Case attribute methods
    @abstractmethod
    def case_types(self):
        pass

    @abstractmethod
    def case_location(self):
        pass

    # Case modification methods
    @abstractmethod
    def delete_case(self, case):
        pass

    @abstractmethod
    def assign_user_to_case(self, case, user, role):
        pass

    @abstractmethod
    def get_decision(self):
        pass
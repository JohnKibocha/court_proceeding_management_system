
from abc import ABC, abstractmethod
from court_proceedings_management_application.models import Court

class CourtInterface(ABC):
    # Court creation methods
    @abstractmethod
    def create_court(self, **kwargs):
        pass

    # Court retrieval methods
    @abstractmethod
    def get_court_by_id(self, court_id):
        pass

    @abstractmethod
    def get_all_courts(self):
        pass

    @abstractmethod
    def get_court_by_name(self, name):
        pass

    # Court information methods
    @abstractmethod
    def court_types(self):
        pass

    @abstractmethod
    def court_location(self):
        pass

    # Court deletion methods
    @abstractmethod
    def delete_court(self, court):
        pass
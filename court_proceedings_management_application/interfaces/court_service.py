
from court_proceedings_management_application.interfaces.court_database import CourtDatabase, CourtDoesNotExist
from court_proceedings_management_application.interfaces.court_interface import CourtInterface
from court_proceedings_management_application.models import Court


class CourtService(CourtInterface):
    def __init__(self):
        self.court_database = CourtDatabase()

    # Court creation methods
    def create_court(self, **kwargs):
        return self.court_database.create_court(**kwargs)

    # Court retrieval methods
    def get_court_by_id(self, court_id):
        try:
            return self.court_database.get_court_by_id(court_id)
        except CourtDoesNotExist as e:
            print(e)
            return None

    def get_all_courts(self):
        return self.court_database.get_all_courts()

    def get_court_by_name(self, name):
        try:
            return self.court_database.get_court_by_name(name)
        except CourtDoesNotExist as e:
            print(e)
            return None

    # Court information methods
    def court_types(self):
        return self.court_database.court_types()

    def court_location(self):
        return self.court_database.court_location()

    # Court deletion methods
    def delete_court(self, court):
        self.court_database.delete_court(court)
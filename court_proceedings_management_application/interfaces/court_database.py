
from court_proceedings_management_application.interfaces.court_interface import CourtInterface
from court_proceedings_management_application.models import Court, User


class CourtDoesNotExist(Exception):
    pass


class CourtDatabase(CourtInterface):
    # Court creation methods
    def create_court(self, **kwargs):
        court = Court(**kwargs)
        court.save()
        return court

    # Court retrieval methods
    def get_court_by_id(self, court_id):
        try:
            return Court.objects.get(id=court_id)
        except:
            raise CourtDoesNotExist(f'Court with id {court_id} does not exist')

    def get_all_courts(self):
        return Court.objects.all()

    def get_court_by_name(self, name):
        try:
            return Court.objects.get(name=name)
        except:
            raise CourtDoesNotExist(f'Court with name {name} does not exist')

    # Court information methods
    def court_types(self):
        return Court.COURT_TYPES

    def court_location(self):
        return User.COUNTY_CHOICES

    # Court deletion methods
    def delete_court(self, court):
        court.delete()
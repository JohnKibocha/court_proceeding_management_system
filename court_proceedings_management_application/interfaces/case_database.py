from django.shortcuts import get_object_or_404

from court_proceedings_management_application.interfaces.case_interface import CaseInterface
from court_proceedings_management_application.models import Case, User


class CaseDoesNotExist(Exception):
    pass


class CaseDatabase(CaseInterface):
    # Case creation methods
    def create_case(self, **kwargs):
        case = Case(**kwargs)
        case.save()
        return case

    # Case retrieval methods
    def get_case_by_id(self, case_id):
        try:
            # use get_object_or_404 to raise a 404 error if the case does not exist
            return get_object_or_404(Case, id=case_id)
        except:
            raise CaseDoesNotExist(f'Case with id {case_id} does not exist')

    def get_all_cases(self):
        return Case.objects.all()

    def get_case_by_name(self, name):
        return Case.objects.get(name=name)

    # Case attribute methods
    def case_types(self):
        case_types = Case.CASE_TYPES
        return case_types

    def case_location(self):
        location = User.COUNTY_CHOICES
        return location

    # Case modification methods
    def delete_case(self, case):
        case.delete()

    def assign_user_to_case(self, case, user, role):
        if role == 'plaintiff':
            case.plaintiffs.add(user)
        elif role == 'defendant':
            case.defendants.add(user)
        elif role == 'judge':
            case.judges.add(user)
        elif role == 'clerk':
            case.clerks.add(user)
        elif role == 'lawyer':
            case.lawyers.add(user)
        elif role == 'observer':
            case.observers.add(user)
        elif role == 'amicus':
            case.amicus.add(user)
        else:
            raise Exception('The role provided is does not exist.')
        case.save()

    def get_decision(self):
        return Case.DECISION_CHOICES
from django.shortcuts import get_object_or_404

from court_proceedings_management_application.interfaces.case_proceeding_interface import CaseProceedingInterface
from court_proceedings_management_application.models import CaseProceeding, Relief


class CaseProceedingDoesNotExist(Exception):
    pass


class CaseProceedingDatabase(CaseProceedingInterface):
    # Case proceeding related methods
    def get_case_proceeding_by_id(self, case_proceeding_id):
        try:
            return get_object_or_404(CaseProceeding, id=case_proceeding_id)
        except CaseProceeding.DoesNotExist:
            raise CaseProceedingDoesNotExist

    def create_case_proceeding(self, case_id, **kwargs):
        case_proceeding = CaseProceeding(case_id=case_id, **kwargs)
        case_proceeding.save()
        return case_proceeding

    def update_case_proceeding(self, case_proceeding_id, **kwargs):
        case_proceeding = self.get_case_proceeding_by_id(case_proceeding_id)
        for key, value in kwargs.items():
            setattr(case_proceeding, key, value)
        case_proceeding.save()
        return case_proceeding

    def delete_case_proceeding(self, case_proceeding_id):
        case_proceeding = self.get_case_proceeding_by_id(case_proceeding_id)
        case_proceeding.delete()
        return case_proceeding

    # case proceeding permission methods
    def grant_case_proceeding_edit_permission(self, case_proceeding, user):
        case_proceeding.editors.add(user)
        case_proceeding.save()
        return case_proceeding

    # case proceeding retrieval methods
    def get_all_case_proceedings(self):
        return CaseProceeding.objects.all()

    def get_case_proceedings(self, case_id):
        return CaseProceeding.objects.filter(case_id=case_id)

    def get_case_proceeding_by_date(self, case_id, date):
        return CaseProceeding.objects.filter(case_id=case_id, date=date)

    def get_case_proceeding_by_case(self, case_id):
        return CaseProceeding.objects.filter(case_id=case_id)

    def get_document_types(self):
        return CaseProceeding.DOCUMENT_TYPES

    def get_document_confidentiality(self):
        return CaseProceeding.CONFIDENTIALITY_LEVELS

    def get_document_types_for_role(self, role):
        all_document_types = self.get_document_types()
        if role == 'clerk':
            return all_document_types
        elif role == 'judge':
            return [document_type for document_type in all_document_types if
                    document_type[0] in ['order', 'report', 'judgement', 'opinion', 'notice', 'warrant', 'summons',
                                         'verdict', 'sentence', 'ruling', 'decree', 'directive', 'mandate', 'injunction',
                                         'citation', 'subpoena', 'transcript']]
        elif role == 'participant':
            return [document_type for document_type in all_document_types if
                    document_type[0] in ['evidence', 'brief', 'complaint', 'declaration', 'deposition', 'pleading',
                                         'petition', 'reply', 'will', 'subpoena', 'transcript', 'appeal']]
        elif role == 'lawyer':
            return [document_type for document_type in all_document_types if
                    document_type[0] in ['evidence', 'motion', 'agreement', 'report', 'statement', 'notice', 'affidavit',
                                         'memorandum', 'brief', 'complaint', 'declaration', 'deposition', 'pleading',
                                         'petition', 'reply', 'will', 'subpoena', 'transcript', 'appeal', 'writ']]
        elif role == 'admin':
            return []
        else:
            return []

    # relief handling methods
    def create_relief(self, participant, case_proceeding, court, relief_type, verdict, value):
        relief = Relief(participant=participant, case_proceeding=case_proceeding, court=court, relief_type=relief_type,
                        verdict=verdict, value=value)
        relief.save()
        return relief

    def get_relief_by_id(self, relief_id):
        return Relief.objects.get(id=relief_id)

    def update_relief(self, relief_id, participant=None, case_proceeding=None, court=None, relief_type=None,
                      verdict=None, value=None):
        relief = self.get_relief_by_id(relief_id)
        if participant:
            relief.participant = participant
        if case_proceeding:
            relief.case_proceeding = case_proceeding
        if court:
            relief.court = court
        if relief_type:
            relief.relief_type = relief_type
        if verdict:
            relief.verdict = verdict
        if value:
            relief.value = value
        relief.save()
        return relief

    def get_relief_by_case_proceeding(self, case_proceeding_id):
        return Relief.objects.filter(case_proceeding=case_proceeding_id)

    def get_relief_by_participant(self, participant, case_proceeding_id):
        return Relief.objects.filter(participant=participant, case_proceeding=case_proceeding_id)

    def delete_relief(self, relief_id):
        relief = self.get_relief_by_id(relief_id)
        relief.delete()

    def get_relief_types(self):
        return Relief.RELIEF_TYPES
    def get_verdicts(self):
        return Relief.VERDICT_CHOICES

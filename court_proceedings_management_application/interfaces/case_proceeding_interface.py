from abc import abstractmethod, ABC


class CaseProceedingInterface(ABC):
    # Case proceeding related methods
    @abstractmethod
    def get_case_proceeding_by_id(self, case_proceeding_id):
        pass

    @abstractmethod
    def create_case_proceeding(self, case_id, **kwargs):
        pass

    @abstractmethod
    def update_case_proceeding(self, case_proceeding_id, **kwargs):
        pass

    @abstractmethod
    def delete_case_proceeding(self, case_proceeding_id):
        pass

    # case proceeding permission methods
    @abstractmethod
    def grant_case_proceeding_edit_permission(self, case_proceeding, user):
        pass

    # case proceeding retrieval methods
    @abstractmethod
    def get_all_case_proceedings(self):
        pass

    @abstractmethod
    def get_case_proceedings(self, case_id):
        pass

    @abstractmethod
    def get_case_proceeding_by_date(self, case_id, date):
        pass

    @abstractmethod
    def get_case_proceeding_by_case(self, case_id):
        pass

    @abstractmethod
    def get_document_types(self):
        pass

    @abstractmethod
    def get_document_confidentiality(self):
        pass

    @abstractmethod
    def get_document_types_for_role(self, role):
        pass

    @abstractmethod
    def get_verdicts(self):
        pass

    # relief handling methods
    @abstractmethod
    def create_relief(self, participant, case_proceeding, court, relief_type, verdict, value):
        pass

    @abstractmethod
    def get_relief_types(self):
        pass

    @abstractmethod
    def get_relief_by_id(self, relief_id):
        pass

    @abstractmethod
    def get_relief_by_case_proceeding(self, case_proceeding_id):
        pass

    @abstractmethod
    def get_relief_by_participant(self, participant, case_proceeding_id):
        pass

    @abstractmethod
    def update_relief(self, relief_id, participant=None, case_proceeding=None, court=None, relief_type=None, verdict=None, value=None):
        pass

    @abstractmethod
    def delete_relief(self, relief_id):
        pass


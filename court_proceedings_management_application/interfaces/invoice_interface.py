from abc import ABC, abstractmethod


class InvoiceInterface(ABC):

    # Invoice creation methods
    @abstractmethod
    def create_invoice(self, **kwargs):
        pass

    # Invoice retrieval methods
    @abstractmethod
    def get_invoice_by_id(self, invoice_id):
        pass

    @abstractmethod
    def get_invoice_by_invoice_id(self, invoice_id):
        pass

    @abstractmethod
    def get_all_invoices(self):
        pass

    @abstractmethod
    def get_invoice_by_name(self, name):
        pass

    # Invoice attribute methods
    @abstractmethod
    def get_invoice_types(self):
        pass

    @abstractmethod
    def get_invoice_status(self):
        pass

    # Invoice modification methods
    @abstractmethod
    def delete_invoice(self, invoice):
        pass

    @abstractmethod
    def assign_user_to_invoice(self, invoice, user, role):
        pass

    # Invoice retrieval methods
    @abstractmethod
    def get_invoice_by_case_id(self, case_id):
        pass

    @abstractmethod
    def get_invoice_by_participant(self, participant):
        pass

    @abstractmethod
    def get_invoice_by_status(self, status):
        pass

    @abstractmethod
    def get_invoice_by_date(self, date):
        pass

    @abstractmethod
    def get_invoice_by_amount(self, amount):
        pass

    @abstractmethod
    def get_invoice_by_case_proceeding(self, case_proceeding):
        pass

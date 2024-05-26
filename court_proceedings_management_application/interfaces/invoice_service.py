from court_proceedings_management_application.interfaces.invoice_database import InvoiceDatabase
from court_proceedings_management_application.interfaces.invoice_interface import InvoiceInterface


class InvoiceService(InvoiceInterface):

    def __init__(self):
        self.invoice_database = InvoiceDatabase()

    def create_invoice(self, **kwargs):
        return self.invoice_database.create_invoice(**kwargs)

    def get_invoice_by_id(self, invoice_id):
        return self.invoice_database.get_invoice_by_id(invoice_id)

    def get_invoice_by_invoice_id(self, invoice_id):
        return self.invoice_database.get_invoice_by_invoice_id(invoice_id)

    def get_all_invoices(self):
        return self.invoice_database.get_all_invoices()

    def get_invoice_by_name(self, name):
        return self.invoice_database.get_invoice_by_name(name)

    def get_invoice_types(self):
        return self.invoice_database.get_invoice_types()

    def get_invoice_status(self):
        return self.invoice_database.get_invoice_status()

    def delete_invoice(self, invoice):
        return self.invoice_database.delete_invoice(invoice)

    def assign_user_to_invoice(self, invoice, user, role):
        return self.invoice_database.assign_user_to_invoice(invoice, user, role)

    def get_invoice_by_case_id(self, case_id):
        return self.invoice_database.get_invoice_by_case_id(case_id)

    def get_invoice_by_participant(self, participant):
        return self.invoice_database.get_invoice_by_participant(participant)

    def get_invoice_by_status(self, status):
        return self.invoice_database.get_invoice_by_status(status)

    def get_invoice_by_date(self, date):
        return self.invoice_database.get_invoice_by_date(date)

    def get_invoice_by_amount(self, amount):
        return self.invoice_database.get_invoice_by_amount(amount)

    def get_invoice_by_case_proceeding(self, case_proceeding):
        return self.invoice_database.get_invoice_by_case_proceeding(case_proceeding)

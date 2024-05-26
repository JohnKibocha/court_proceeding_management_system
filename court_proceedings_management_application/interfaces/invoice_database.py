from court_proceedings_management_application.interfaces.invoice_interface import InvoiceInterface
from court_proceedings_management_application.models import Invoice


class InvoiceDoesNotExist(Exception):
    pass


class InvoiceDatabase(InvoiceInterface):

    def create_invoice(self, **kwargs):
        invoice = Invoice(**kwargs)
        invoice.save()
        return invoice

    def get_invoice_by_id(self, invoice_id):
        try:
            return Invoice.objects.get(id=invoice_id)
        except:
            raise InvoiceDoesNotExist(f'Invoice with id {invoice_id} does not exist')

    def get_invoice_by_invoice_id(self, invoice_id):
        try:
            return Invoice.objects.get(invoice_id=invoice_id)
        except:
            raise InvoiceDoesNotExist(f'Invoice with invoice id {invoice_id} does not exist')

    def get_all_invoices(self):
        return Invoice.objects.all()

    def get_invoice_by_name(self, name):
        try:
            return Invoice.objects.get(name=name)
        except:
            raise InvoiceDoesNotExist(f'Invoice with name {name} does not exist')

    def get_invoice_types(self):
        return Invoice.INVOICE_TYPES

    def get_invoice_status(self):
        return Invoice.INVOICE_STATUS

    def delete_invoice(self, invoice):
        invoice.delete()

    def assign_user_to_invoice(self, invoice, user, role):
        invoice.users.add(user, through_defaults={'role': role})
        invoice.save()

    def get_invoice_by_case_id(self, case_id):
        return Invoice.objects.filter(case_id=case_id)

    def get_invoice_by_participant(self, participant):
        return Invoice.objects.filter(participant=participant)

    def get_invoice_by_status(self, status):
        return Invoice.objects.filter(status=status)

    def get_invoice_by_date(self, date):
        return Invoice.objects.filter(date=date)

    def get_invoice_by_amount(self, amount):
        return Invoice.objects.filter(amount=amount)

    def get_invoice_by_case_proceeding(self, case_proceeding):
        return Invoice.objects.filter(case_proceeding=case_proceeding)

from court_proceedings_management_application.models import Transaction
from court_proceedings_management_application.interfaces.payment_interface import PaymentInterface

class PaymentDoesNotExist(Exception):
    pass


class PaymentDatabase(PaymentInterface):
    # Payment creation methods
    def create_payment(self, **kwargs):
        transaction = Transaction(**kwargs)
        transaction.save()
        return transaction

    # Payment retrieval methods
    def get_payment_by_id(self, payment_id):
        return Transaction.objects.get(id=payment_id)

    def get_all_payments(self):
        return Transaction.objects.all()

    def get_payment_by_case_id(self, case_id):
        return Transaction.objects.get(case_id=case_id)

    def get_payment_by_participant(self, participant):
        return Transaction.objects.filter(participant=participant)

    # Payment deletion methods
    def delete_payment(self, payment):
        payment.delete()

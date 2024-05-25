from court_proceedings_management_application.interfaces.payment_interface import PaymentInterface
from court_proceedings_management_application.models import Transaction

class PaymentDoesNotExist(Exception):
    pass

class PaymentDatabase(PaymentInterface):
    # Payment creation methods
    def create_payment(self, **kwargs):
        transaction= Transaction(**kwargs)
        transaction.save()
        return transaction

    # Payment retrieval methods
    def get_payment_by_id(self, payment_id):
        try:
            return Transaction.objects.get(id=payment_id)
        except:
            raise PaymentDoesNotExist(f'Payment with id {payment_id} does not exist')

    def get_all_payments(self):
        return Transaction.objects.all()

    def get_payment_by_case_id(self, case_id):
        try:
            return Transaction.objects.get(case_id=case_id)
        except:
            raise PaymentDoesNotExist(f'Payment with case id {case_id} does not exist')

    # Payment deletion methods
    def delete_payment(self, payment):
        payment.delete()


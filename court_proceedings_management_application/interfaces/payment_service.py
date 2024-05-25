from court_proceedings_management_application.interfaces.payment_database import PaymentDatabase
from court_proceedings_management_application.interfaces.payment_interface import PaymentInterface

class PaymentDoesNotExist(Exception):
    pass

class PaymentService(PaymentInterface):
    def __init__(self):
        self.payment_database = PaymentDatabase()

    # Payment creation methods
    def create_payment(self, **kwargs):
        return self.payment_database.create_payment(**kwargs)

    # Payment retrieval methods
    def get_payment_by_id(self, payment_id):
        try:
            return self.payment_database.get_payment_by_id(payment_id)
        except PaymentDoesNotExist as e:
            print(e)
            return None

    def get_all_payments(self):
        return self.payment_database.get_all_payments()

    def get_payment_by_case_id(self, case_id):
        try:
            return self.payment_database.get_payment_by_case_id(case_id)
        except PaymentDoesNotExist as e:
            print(e)
            return None

    # Payment deletion methods
    def delete_payment(self, payment):
        self.payment_database.delete_payment(payment)
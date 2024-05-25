from abc import ABC, abstractmethod

class PaymentInterface(ABC):
    # Payment creation methods
    @abstractmethod
    def create_payment(self, **kwargs):
        pass

    # Payment retrieval methods
    @abstractmethod
    def get_payment_by_id(self, payment_id):
        pass

    @abstractmethod
    def get_all_payments(self):
        pass

    @abstractmethod
    def get_payment_by_case_id(self, case_id):
        pass

    # Payment deletion methods
    @abstractmethod
    def delete_payment(self, payment):
        pass


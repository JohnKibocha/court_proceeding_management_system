from abc import ABC

from court_proceedings_management_application.interfaces.payment_queue_database import PaymentQueueDatabase
from court_proceedings_management_application.interfaces.payment_queue_interface import PaymentQueueInterface


class PaymentQueueService(PaymentQueueInterface, ABC):
    def __init__(self):
        self.payment_queue_database = PaymentQueueDatabase()

    # create, update, delete operations
    def create_payment_queue(self, **kwargs):
        return self.payment_queue_database.create_payment_queue(**kwargs)

    def update_payment_queue(self, payment_queue_id, **kwargs):
        return self.payment_queue_database.update_payment_queue(payment_queue_id, **kwargs)

    def delete_payment_queue(self, payment_queue_id):
        return self.payment_queue_database.delete_payment_queue(payment_queue_id)

    # read operations
    def get_payment_queue_by_id(self, payment_queue_id):
        return self.payment_queue_database.get_payment_queue_by_id(payment_queue_id)

    def get_all_payment_queues(self):
        return self.payment_queue_database.get_all_payment_queues()

    def get_payment_queue_by_checkout_request_id(self, checkout_request_id):
        return self.payment_queue_database.get_payment_queue_by_checkout_request_id(checkout_request_id)

    def get_payment_queue_by_status(self, status):
        return self.payment_queue_database.get_payment_queue_by_status(status)

    def get_payment_queue_by_phone_number(self, phone_number):
        return self.payment_queue_database.get_payment_queue_by_phone_number(phone_number)

    def get_payment_queue_by_invoice(self, invoice):
        return self.payment_queue_database.get_payment_queue_by_invoice(invoice)

    def get_payment_queue_by_date(self, date):
        return self.payment_queue_database.get_payment_queue_by_date(date)



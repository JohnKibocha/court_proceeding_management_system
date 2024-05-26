from abc import ABC

from court_proceedings_management_application.interfaces.payment_queue_interface import PaymentQueueInterface
from court_proceedings_management_application.models import PaymentQueue


class PaymentQueueDatabase(PaymentQueueInterface, ABC):
    # create, update, delete operations
    def create_payment_queue(self, **kwargs):
        payment_queue = PaymentQueue(**kwargs)
        payment_queue.save()
        return payment_queue

    def update_payment_queue(self, payment_queue_id, **kwargs):
        payment_queue = self.get_payment_queue_by_id(payment_queue_id)
        for key, value in kwargs.items():
            setattr(payment_queue, key, value)
        payment_queue.save()
        return payment_queue

    def delete_payment_queue(self, payment_queue_id):
        payment_queue = self.get_payment_queue_by_id(payment_queue_id)
        payment_queue.delete()

    # read operations
    def get_payment_queue_by_id(self, payment_queue_id):
        return PaymentQueue.objects.get(id=payment_queue_id)

    def get_all_payment_queues(self):
        return PaymentQueue.objects.all()

    def get_payment_queue_by_checkout_request_id(self, checkout_request_id):
        return PaymentQueue.objects.get(checkout_request_id=checkout_request_id)

    def get_payment_queue_by_status(self, status):
        return PaymentQueue.objects.filter(status=status)

    def get_payment_queue_by_phone_number(self, phone_number):
        return PaymentQueue.objects.filter(phone_number=phone_number)

    def get_payment_queue_by_invoice(self, invoice):
        return PaymentQueue.objects.filter(invoice=invoice)

    def get_payment_queue_by_date(self, date):
        return PaymentQueue.objects.filter(date=date)



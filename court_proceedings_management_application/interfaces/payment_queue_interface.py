from abc import abstractmethod, ABC


class PaymentQueueInterface(ABC):
    # create, update, delete operations
    @abstractmethod
    def create_payment_queue(self, **kwargs):
        pass

    @abstractmethod
    def update_payment_queue(self, payment_queue_id, **kwargs):
        pass

    @abstractmethod
    def delete_payment_queue(self, payment_queue_id):
        pass

    # read operations
    @abstractmethod
    def get_payment_queue_by_id(self, payment_queue_id):
        pass

    @abstractmethod
    def get_all_payment_queues(self):
        pass

    @abstractmethod
    def get_payment_queue_by_checkout_request_id(self, checkout_request_id):
        pass

    @abstractmethod
    def get_payment_queue_by_status(self, status):
        pass

    @abstractmethod
    def get_payment_queue_by_phone_number(self, phone_number):
        pass

    @abstractmethod
    def get_payment_queue_by_invoice(self, invoice):
        pass

    @abstractmethod
    def get_payment_queue_by_date(self, date):
        pass

from abc import ABC, abstractmethod


class ContactInterface(ABC):
    @abstractmethod
    def send_email(self, contact):
        pass

    @abstractmethod
    def save_contact(self, contact):
        pass

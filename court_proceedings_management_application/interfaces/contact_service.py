
from court_proceedings_management_application.interfaces.contact_database import ContactDatabase
from court_proceedings_management_application.interfaces.contact_interface import ContactInterface


class ContactService(ContactInterface):
    def __init__(self):
        self.contact_database = ContactDatabase()

    def send_email(self, contact):
        self.contact_database.send_email(contact)

    def save_contact(self, contact):
        self.contact_database.save_contact(contact)
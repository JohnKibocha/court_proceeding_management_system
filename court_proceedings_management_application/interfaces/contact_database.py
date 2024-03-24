import os

from django.core.mail import send_mail

from court_proceedings_management_application.interfaces.contact_interface import ContactInterface


class ContactDatabase(ContactInterface):
    def send_email(self, contact):
        subject = '(Courtix) New Message from ' + contact.first_name + ': ' + contact.subject
        message = contact.message
        recipient_list = [os.environ['ADMIN_EMAIL']]
        email_from = contact.email
        send_mail(subject, message, email_from, recipient_list)

    def save_contact(self, contact):
        contact.save()

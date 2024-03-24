
import os

from django.contrib.auth.hashers import make_password
from court_proceedings_management_application.models import User
from court_proceedings_management_application.interfaces.admin_interface import AdminInterface


class AdminDoesNotExist(Exception):
    pass


class AdminDatabase(AdminInterface):
    # Admin related methods
    def get_admin(self):
        try:
            return User.objects.get(username='admin')
        except User.DoesNotExist:
            return None

    def create_admin(self):
        admin = User(
            first_name='Admin', last_name='User', username='admin', role='admin', password=make_password(os.environ['ADMIN_PASSWORD']),
            county_of_residence='Nairobi',
            phone_number='0113187222', national_id=12345678, email=os.environ['ADMIN_EMAIL'], is_staff=True,
            is_active=True, is_superuser=True, is_approved=True, gender='prefer not to say', tribe='N/A',
            date_of_birth='2001-01-01', address='N/A', profile_image='../static/images/admin-profile.png'
        )
        admin.save()
        return admin

    # User registration and approval methods
    def register_user(self, role, **kwargs):
        user = User(role=role, is_approved=True, **kwargs)
        user.is_staff = True
        user.save()
        return user

    def approve_user(self, user):
        user.is_approved = True
        user.is_active = True
        user.save()
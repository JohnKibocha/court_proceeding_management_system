
from court_proceedings_management_application.interfaces.user_database import UserDatabase, UserDoesNotExist
from court_proceedings_management_application.interfaces.user_interface import UserInterface
from court_proceedings_management_application.models import User


class ClerkService(UserInterface):
    def __init__(self):
        self.user_database = UserDatabase()

    # User creation methods
    def register_user(self, role, **kwargs):
        try:
            user = self.user_database.create_user(role, **kwargs)
            user.is_approved = True
            user.is_staff = True
            user.save()
            return user
        except UserDoesNotExist as e:
            print(e)
            return None

    # User approval methods
    def approve_user(self, user):
        self.user_database.approve_user(user)
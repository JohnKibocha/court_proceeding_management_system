
from court_proceedings_management_application.interfaces.user_database import UserDatabase, UserDoesNotExist
from court_proceedings_management_application.interfaces.user_interface import UserInterface
from court_proceedings_management_application.models import Court


class UserService(UserInterface):
    def __init__(self):
        self.user_database = UserDatabase()

    # User creation methods
    def create_user(self, role, **kwargs):
        return self.user_database.create_user(role, **kwargs)

    # User approval methods
    def approve_user(self, user):
        self.user_database.approve_user(user)

    # User retrieval methods
    def get_user(self, username):
        try:
            return self.user_database.get_user(username)
        except UserDoesNotExist as e:
            print(e)
            return None

    def get_user_info(self, username):
        try:
            return self.user_database.get_user_info(username)
        except UserDoesNotExist as e:
            print(e)
            return None

    def get_all_users(self):
        return self.user_database.get_all_users()

    def get_user_by_id(self, user_id):
        try:
            return self.user_database.get_user_by_id(user_id)
        except UserDoesNotExist as e:
            print(e)
            return None

    def get_user_by_role(self, role):
        try:
            return self.user_database.get_user_by_role(role)
        except UserDoesNotExist as e:
            print(e)
            return None

    # User modification methods
    def delete_user(self, user):
        self.user_database.delete_user(user)

    def update_user(self, user_id, **kwargs):
        return self.user_database.update_user(user_id, **kwargs)

    # User assignment methods
    def assign_user_creator(self, user, creator):
        self.user_database.assign_user_creator(user, creator)

    def assign_user_to_court(self, user, court):
        if user.role not in ['judge', 'clerk'] or user.courts.count() == 0:
            user.courts.add(court)
        else:
            raise Exception('A judge or clerk cannot be assigned to more than one court.')

    def remove_user_from_court(self, user, court):
        if court in user.courts.all():
            user.courts.remove(court)
        else:
            raise Exception('The user is not assigned to the specified court.')

    def auto_assign_user_to_court(self, user):
        matching_courts = Court.objects.filter(location=user.county_of_residence)
        for court in matching_courts:
            if user.role not in ['judge', 'clerk'] or user.courts.count() == 0:
                user.courts.add(court)

    # Methods to get additional user information
    def get_counties(self):
        return self.user_database.get_counties()

    def get_tribes(self):
        return self.user_database.get_tribes()
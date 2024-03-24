
from abc import abstractmethod


class UserInterface:
    # User creation methods
    @abstractmethod
    def create_user(self, role, **kwargs):
        pass

    # User approval methods
    @abstractmethod
    def approve_user(self, user):
        pass

    # User retrieval methods
    @abstractmethod
    def get_user(self, username):
        pass

    @abstractmethod
    def get_user_info(self, username):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id):
        pass

    @abstractmethod
    def get_user_by_role(self, role):
        pass

    # User modification methods
    @abstractmethod
    def delete_user(self, user):
        pass

    @abstractmethod
    def update_user(self, user_id, **kwargs):
        pass

    # User assignment methods
    @abstractmethod
    def assign_user_creator(self, user, creator):
        pass

    @abstractmethod
    def assign_user_to_court(self, user, court):
        pass

    @abstractmethod
    def remove_user_from_court(self, user, court):
        pass

    @abstractmethod
    def auto_assign_user_to_court(self, user):
        pass

    # Methods to get additional user information
    @abstractmethod
    def get_counties(self):
        pass

    @abstractmethod
    def get_tribes(self):
        pass
from abc import abstractmethod


class AdminInterface:
    # Admin related methods
    @abstractmethod
    def get_admin(self):
        pass

    @abstractmethod
    def create_admin(self):
        pass

    # User registration and approval methods
    @abstractmethod
    def register_user(self, role, **kwargs):
        pass

    @abstractmethod
    def approve_user(self, user):
        pass

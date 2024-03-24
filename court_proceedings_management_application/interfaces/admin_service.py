
from court_proceedings_management_application.interfaces.admin_database import AdminDoesNotExist, AdminDatabase
from court_proceedings_management_application.interfaces.admin_interface import AdminInterface


class AdminService(AdminInterface):
    def __init__(self):
        self.admin_database = AdminDatabase()

    # Admin related methods
    def get_admin(self):
        return self.admin_database.get_admin()

    def create_admin(self):
        return self.admin_database.create_admin()

    # User registration and approval methods
    def register_user(self, role, **kwargs):
        try:
            return self.admin_database.register_user(role, **kwargs)

        except AdminDoesNotExist as e:
            print(e)
            return None

    def approve_user(self, user):
        self.admin_database.approve_user(user)
from court_proceedings_management_application.interfaces.admin_service import AdminService
from court_proceedings_management_application.interfaces.clerk_service import ClerkService
from court_proceedings_management_application.interfaces.user_database import UserDatabase
from court_proceedings_management_application.interfaces.user_service import UserService
from court_proceedings_management_application.models import User


class RegistrationService:
    def __init__(self, admin_service, clerk_service):
        self.admin_service = AdminService()
        self.clerk_service = ClerkService()
        self.user_service = UserService()

    def register_user(self, role, creator=None, **kwargs):
        if role in ['admin', 'clerk', 'judge']:
            return self.admin_service.register_user(role, **kwargs)
        elif role in ['participant', 'lawyer', 'observer']:
            return self.clerk_service.register_user(role, **kwargs)
        else:
            user = self.user_service.create_user(role, **kwargs)

        self.user_service.assign_user_creator(user, creator)
        return user

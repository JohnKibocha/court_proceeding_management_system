
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from court_proceedings_management_application.interfaces.user_interface import UserInterface
from court_proceedings_management_application.models import User


class UserDoesNotExist(Exception):
    pass


class UserDatabase(UserInterface):
    # User creation methods
    def create_user(self, role, **kwargs):
        user = User(role=role, is_approved=False, **kwargs)
        user.is_staff = True
        user.save()
        return user

    # User approval methods
    def approve_user(self, user):
        user.is_approved = True
        user.save()

    # User retrieval methods
    def get_user(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return UserDoesNotExist(f'User with username {username} does not exist')

    def get_user_info(self, username):
        try:
            return get_object_or_404(User, username=username)
        except User.DoesNotExist:
            return UserDoesNotExist(f'User with username {username} does not exist')

    def get_all_users(self):
        return User.objects.all()

    def get_user_by_id(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return UserDoesNotExist(f'User with id {user_id} does not exist')

    def get_user_by_role(self, role):
        try:
            return User.objects.filter(role=role)
        except User.DoesNotExist:
            return UserDoesNotExist(f'User with role {role} does not exist')

    # User modification methods
    def delete_user(self, user):
        user.delete()

    def update_user(self, user_id, **kwargs):
        user = self.get_user_by_id(user_id)
        for key, value in kwargs.items():
            setattr(user, key, value)
        user.save()
        return user

    # User assignment methods
    def assign_user_creator(self, user, creator):
        if creator is None:
            user.created_by = user
        else:
            if creator.is_authenticated and creator.role == 'clerk':
                user.created_by = creator
        user.save()

    # Methods to get additional user information
    def get_counties(self):
        counties = User.COUNTY_CHOICES
        return counties

    def get_tribes(self):
        tribes = User.TRIBE_CHOICES
        return tribes
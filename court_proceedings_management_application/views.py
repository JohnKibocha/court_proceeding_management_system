import json
import logging
import math
from datetime import datetime
from io import BytesIO

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LogoutView
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, request
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse
from django.utils import html
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django_daraja.mpesa.core import MpesaClient
from xhtml2pdf import pisa

from court_proceedings_management_application.forms import CaseProceedingForm
from court_proceedings_management_application.interfaces.admin_service import AdminService
from court_proceedings_management_application.interfaces.case_proceeding_service import CaseProceedingService
from court_proceedings_management_application.interfaces.case_service import CaseService
from court_proceedings_management_application.interfaces.clerk_service import ClerkService
from court_proceedings_management_application.interfaces.contact_service import ContactService
from court_proceedings_management_application.interfaces.court_service import CourtService
from court_proceedings_management_application.interfaces.invoice_service import InvoiceService
from court_proceedings_management_application.interfaces.payment_queue_service import PaymentQueueService
from court_proceedings_management_application.interfaces.payment_service import PaymentService
from court_proceedings_management_application.interfaces.registration_service import RegistrationService
from court_proceedings_management_application.interfaces.user_service import UserDoesNotExist
from court_proceedings_management_application.interfaces.user_service import UserService
from court_proceedings_management_application.models import Contact


## system-wide views
class IndexView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.admin_service = AdminService()

    def get(self, request):
        self.ensure_admin_exists()
        return render(request, 'index.html')

    # first check if admin exists and if not create one
    def ensure_admin_exists(self):
        admin = self.admin_service.get_admin()
        if admin is None:
            try:
                self.admin_service.create_admin()
                print(f'Admin User created successfully')
            except:
                print(f'Failed to create Admin User')
        else:
            print(f'Admin User already exists')


class ContactView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.contact_service = ContactService()

    def get(self, request):
        created_on = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return render(request, 'index.html', {'created_on': created_on})

    def post(self, request):
        # handle contact form submission
        if request.method == 'POST':
            contact = Contact(
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'] if 'last_name' in request.POST else None,
                email=request.POST['email'],
                subject=request.POST['subject'],
                message=request.POST['message'],
                phone=request.POST['phone'] if 'phone' in request.POST else None
            )

            contact = self.contact_service.save_contact(contact)
            messages.success(request, 'Your message has been sent successfully', extra_tags='toast')
        return render(request, 'index.html')


class HeaderView(View):
    def get(self, request):
        return render(request, 'index.html')


class FooterView(View):
    def get(self, request):
        return render(request, 'index.html')


class SidebarView(View):
    def get(self, request):
        return render(request, 'sidebar.html')


class SuccessView(View):
    def get(self, request):
        return render(request, 'index.html')


## authentication views
class RegisterView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration_service = RegistrationService(AdminService(), ClerkService())
        self.user_service = UserService()
        self.user_service = UserService()

    def get(self, request):
        counties = self.user_service.get_counties()
        tribes = self.user_service.get_tribes()
        return render(request, 'register.html', {'counties': counties, 'tribes': tribes})

    def post(self, request):
        if request.method == 'POST':
            profile_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
            if profile_image is not None:
                fs = FileSystemStorage()
                filename = fs.save(profile_image.name, profile_image)
                uploaded_file_url = filename
            else:
                uploaded_file_url = None

            # Concatenate the address fields
            postal_code = request.POST.get('postal_code')
            town_city = request.POST.get('town_city')
            building_name = request.POST.get('building_name', '')
            floor_number = request.POST.get('floor_number', '')
            street_name = request.POST.get('street_name', '')

            # first check if the password and confirm password match
            if request.POST['password'] != request.POST['confirm_password']:
                messages.error(request, 'Password and confirm password do not match', extra_tags='toast')
                return render(request, 'register.html')
            else:
                # create user
                user = self.registration_service.register_user(

                    role=request.POST['role'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'] if 'last_name' in request.POST else None,
                    username=request.POST['username'],
                    email=request.POST['email'],
                    national_id=request.POST['national_id'],
                    county_of_residence=request.POST['county_of_residence'],
                    phone_number=request.POST['phone_number'],
                    gender=request.POST['gender'],
                    tribe=request.POST['tribe'],
                    date_of_birth=request.POST['date_of_birth'],
                    address=f'{postal_code}, {building_name}, {floor_number} Floor, {street_name}, {town_city}, Kenya',
                    password=make_password(request.POST['password']),
                    is_active=True,
                    is_staff=False,
                    is_superuser=False,
                    profile_image=uploaded_file_url
                )

            # automatically assign user to court
            self.user_service.auto_assign_user_to_court(user)

            if not user.is_approved:
                messages.success(request, 'Your account has been created successfully. Please wait for approval',
                                 extra_tags='toast')
                messages.warning(request, 'Your account is pending approval', extra_tags='modal')
                return redirect('pending-approval')
            else:
                messages.success(request, 'Your account has been created successfully. You can now login',
                                 extra_tags='toast')
                return redirect('dashboard')

        return render(request, 'register.html')


class PendingApprovalView(View):
    def get(self, request):
        user_id = request.user.id
        return render(request, 'pending-approval.html', {'id': user_id})


# login view
class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        # handle login form submission, authenticate user and redirect to dashboard
        if request.method == 'POST':
            input_username = request.POST['username']
            input_password = request.POST['password']
            user = authenticate(username=input_username, password=input_password)
            if user is not None:
                login(request, user)
                if not user.is_approved:
                    messages.warning(request, 'Your account is pending approval', extra_tags='modal')
                    return redirect('pending-approval')
                else:
                    messages.success(request, 'Login successful', extra_tags='toast')
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password', extra_tags='toast')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid username or password', extra_tags='toast')
            return render(request, 'login.html')


class UserLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.success(self.request, 'You have been logged out successfully', extra_tags='toast')
        return super().get(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('login'))


# views.py
class DashboardView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.court_service = CourtService()
        self.case_service = CaseService()
        self.user_service = UserService()
        self.payment_service = PaymentService()
        self.invoice_service = InvoiceService()
        self.case_proceeding_service = CaseProceedingService()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        print(f'Is {user.username}  authenticated? {user.is_authenticated}')
        user_info = self.user_service.get_user_info(user.username)
        clerks = self.user_service.get_user_by_role('clerk')
        judges = self.user_service.get_user_by_role('judge')
        courts = self.court_service.get_all_courts()
        cases = self.case_service.get_all_cases()
        participants = self.user_service.get_all_users()
        transactions = self.payment_service.get_all_payments()
        invoices = self.invoice_service.get_all_invoices()
        case_documents = self.case_proceeding_service.get_all_case_proceedings()

        context = {
            'user': user,
            'user_info': user_info,
            'clerks': clerks,
            'judges': judges,
            'courts': courts,
            'cases': cases,
            'participants': participants,
            'transactions': transactions,
            'invoices': invoices,
            'case_documents': case_documents
        }

        return render(request, 'dashboard.html', context)


## Admin views
class AdminManageClerksView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        user_info = self.user_service.get_user_info(user.username)

        try:
            clerks = self.user_service.get_user_by_role('clerk')
        except:
            clerks = None
            messages.error(request, 'No clerks found in the database', extra_tags='toast')

        context = {
            'clerks': clerks,
            'user_info': user_info
        }

        return render(request, 'admin-manage-clerk.html', context)


class AdminCreateClerkView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration_service = RegistrationService(AdminService(), ClerkService())
        self.user_service = UserService()
        self.court_service = CourtService()
        self.user_service = UserService()

    def get(self, request):
        counties = self.user_service.get_counties()
        tribes = self.user_service.get_tribes()
        court_objects = self.court_service.get_all_courts()
        user = request.user
        user_info = self.user_service.get_user_info(user.username)

        # if no court in the database, redirect to create court with a message
        if len(court_objects) == 0:
            messages.error(request, 'No courts found in the database. Please create a court first', extra_tags='toast')
            return redirect('admin-create-court')
        else:
            try:
                clerks = self.user_service.get_user_by_role('clerk')
            except:
                clerks = None
                messages.error(request, 'No clerks found in the database', extra_tags='toast')

            context = {
                'counties': counties,
                'tribes': tribes,
                'court_objects': court_objects,
                'user_info': user_info,
                'clerks': clerks
            }

            return render(request, 'admin-create-clerk.html', context)

    def post(self, request):
        if request.method == 'POST':
            profile_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
            if profile_image is not None:
                fs = FileSystemStorage()
                filename = fs.save(profile_image.name, profile_image)
                uploaded_file_url = filename
            else:
                uploaded_file_url = None

            # Concatenate the address fields
            postal_code = request.POST.get('postal_code')
            town_city = request.POST.get('town_city')
            building_name = request.POST.get('building_name', '')
            floor_number = request.POST.get('floor_number', '')
            street_name = request.POST.get('street_name', '')

            # first check if the password and confirm password match
            if request.POST['password'] != request.POST['confirm_password']:
                messages.error(request, 'Password and confirm password do not match', extra_tags='toast')
                return render(request, 'register.html')
            else:
                # create user
                user = self.registration_service.register_user(

                    role=request.POST['role'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'] if 'last_name' in request.POST else None,
                    username=request.POST['username'],
                    email=request.POST['email'],
                    national_id=request.POST['national_id'],
                    county_of_residence=request.POST['county_of_residence'],
                    phone_number=request.POST['phone_number'],
                    gender=request.POST['gender'],
                    tribe=request.POST['tribe'],
                    date_of_birth=request.POST['date_of_birth'],
                    address=f'{postal_code}, {building_name}, {floor_number} Floor, {street_name}, {town_city}, Kenya',
                    password=make_password(request.POST['password']),
                    is_active=True,
                    is_staff=True,
                    is_superuser=False,
                    profile_image=uploaded_file_url
                )

            # assign user to court
            court_id = request.POST['courts']
            court = self.court_service.get_court_by_id(court_id)
            self.user_service.assign_user_to_court(user, court)

            if not user.is_approved:
                messages.success(request, 'The Clerk has been created successfully. Please approve their account',
                                 extra_tags='toast')
                return redirect('admin-manage-clerk')
            else:
                messages.success(request, 'The Clerk has been created successfully. The Clerk can now login',
                                 extra_tags='toast')
                return redirect('admin-manage-clerk')

        return render(request, 'admin-create-clerk.html')


class AdminEditClerkView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration_service = RegistrationService(AdminService(), ClerkService())
        self.user_service = UserService()
        self.court_service = CourtService()

    def get(self, request, user_id):
        counties = self.user_service.get_counties()
        tribes = self.user_service.get_tribes()
        court_objects = self.court_service.get_all_courts()
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        try:
            clerk = self.user_service.get_user_by_id(user_id)
        except UserDoesNotExist:
            messages.error(request, 'Clerk not found', extra_tags='toast')
            return redirect('admin-manage-clerk')

        context = {
            'counties': counties,
            'user_info': user_info,
            'clerk': clerk,
            'tribes': tribes,
            'court_objects': court_objects,

        }

        return render(request, 'admin-edit-clerk.html', context)

    def post(self, request, user_id):
        # check which values have been passed, if they are not empty, update those fields and leave the rest unchanged
        if request.method == 'POST':
            clerk = self.user_service.get_user_by_id(user_id)

            # Concatenate the address fields and set the new values and if not exist retain old ones
            postal_code = request.POST.get('postal_code', '')
            town_city = request.POST.get('town_city', '')
            building_name = request.POST.get('building_name', '')
            floor_number = request.POST.get('floor_number', '')
            street_name = request.POST.get('street_name', '')

            if clerk is not None:

                clerk.first_name = request.POST.get('first_name', clerk.first_name)
                clerk.last_name = request.POST.get('last_name', clerk.last_name)
                clerk.username = request.POST.get('username', clerk.username)
                clerk.email = request.POST.get('email', clerk.email)
                clerk.national_id = request.POST.get('national_id', clerk.national_id)
                clerk.county_of_residence = request.POST.get('county_of_residence', clerk.county_of_residence)
                clerk.phone_number = request.POST.get('phone_number', clerk.phone_number)
                clerk.gender = request.POST.get('gender', clerk.gender)
                clerk.tribe = request.POST.get('tribe', clerk.tribe)
                clerk.date_of_birth = request.POST.get('date_of_birth', clerk.date_of_birth)
                # use the old address if new one not provided
                if postal_code != '' and town_city != '' and building_name != '' and floor_number != '' and street_name != '':
                    clerk.address = f'{postal_code}, {building_name}, {floor_number} Floor, {street_name}, {town_city}, Kenya'
                else:
                    clerk.address = clerk.address

                clerk.password = make_password(request.POST.get('password', None))
                if 'profile_image' in request.FILES:
                    profile_image = request.FILES['profile_image']
                    # Add your validation logic here
                    fs = FileSystemStorage()
                    filename = fs.save(profile_image.name, profile_image)
                    uploaded_file_url = fs.url(filename)
                    clerk.profile_image = uploaded_file_url
                elif not clerk.profile_image:
                    clerk.profile_image = None
                clerk.save()
                messages.success(request, 'Clerk updated successfully', extra_tags='toast')
                return redirect('admin-manage-clerk')
            else:
                messages.error(request, 'Clerk not found', extra_tags='toast')
                return redirect('admin-manage-clerk')


class AdminDeleteClerkView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.user_service = UserService()

    def get(self, request, user_id):
        user = self.user_service.get_user_by_id(user_id)
        if user is not None:
            self.user_service.delete_user(user)
            messages.success(request, 'Clerk deleted successfully', extra_tags='toast')
        else:
            messages.error(request, 'Clerk not found', extra_tags='toast')
        return redirect('admin-manage-clerk')

    def post(self, request, user_id):
        pass


class AdminManageCourtView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.court_service = CourtService()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        courts = self.court_service.get_all_courts()

        context = {
            'courts': courts,
            'user_info': user_info
        }

        return render(request, 'admin-manage-court.html', context)


class AdminCreateCourtView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration_service = RegistrationService(AdminService(), ClerkService())
        self.user_service = UserService()
        self.court_service = CourtService()
        self.user_service = UserService()

    def get(self, request):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)

        court_locations = self.court_service.court_location()
        court_types = self.court_service.court_types()
        try:
            courts = self.court_service.get_all_courts()
        except:
            courts = None
            messages.error(request, 'No Courts found in the database', extra_tags='toast')

        context = {
            'courts': courts,
            'user_info': user_info,
            'court_locations': court_locations,
            'court_types': court_types
        }

        return render(request, 'admin-create-court.html', context)

    def post(self, request):
        if request.method == 'POST':
            court_logo = request.FILES['court_logo'] if 'court_logo' in request.FILES else None
            if court_logo is not None:
                fs = FileSystemStorage()
                filename = fs.save(court_logo.name, court_logo)
                uploaded_file_url = filename
            else:
                uploaded_file_url = None

            # Concatenate the address fields
            postal_code = request.POST.get('postal_code')
            town_city = request.POST.get('town_city')
            building_name = request.POST.get('building_name', '')
            floor_number = request.POST.get('floor_number', '')
            street_name = request.POST.get('street_name', '')

            # create user
            court = self.court_service.create_court(
                name=request.POST['name'],
                court_email=request.POST['court_email'],
                court_phone=request.POST['court_phone'],
                court_address=f'{postal_code}, {building_name}, {floor_number} Floor, {street_name}, {town_city}, Kenya',
                location=request.POST['location'],
                court_type=request.POST['court_type'],
                created_by=request.user,
                court_logo=uploaded_file_url
            )

            if court is not None:
                messages.success(request, 'Court created successfully', extra_tags='toast')
                return redirect('admin-manage-court')
            else:
                messages.error(request, 'Failed to create court', extra_tags='toast')
                return render(request, 'admin-create-court.html')

        return render(request, 'admin-create-court.html')


class AdminEditCourtView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration_service = RegistrationService(AdminService(), ClerkService())
        self.user_service = UserService()
        self.court_service = CourtService()
        self.user_service = UserService()

    def get(self, request, court_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        court = self.court_service.get_court_by_id(court_id)
        court_locations = self.court_service.court_location()
        court_types = self.court_service.court_types()

        context = {
            'court': court,
            'user_info': user_info,
            'court_locations': court_locations,
            'court_types': court_types
        }

        return render(request, 'admin-edit-court.html', context)

    def post(self, request, court_id):
        if request.method == 'POST':
            court = self.court_service.get_court_by_id(court_id)

            # Concatenate the address fields and set the new values and if not exist retain old ones
            postal_code = request.POST.get('postal_code', '')
            town_city = request.POST.get('town_city', '')
            building_name = request.POST.get('building_name', '')
            floor_number = request.POST.get('floor_number', '')
            street_name = request.POST.get('street_name', '')

            if court is not None:

                court.name = request.POST.get('name', court.name)
                court.court_email = request.POST.get('court_email', court.court_email)
                court.location = request.POST.get('location', court.location)
                court.court_phone = request.POST.get('court_phone', court.court_phone)
                court.court_type = request.POST.get('court_type', court.court_type)
                # use the old address if new one not provided
                if postal_code != '' and town_city != '' and building_name != '' and floor_number != '' and street_name != '':
                    court.court_address = f'{postal_code}, {building_name}, {floor_number} Floor, {street_name}, {town_city}, Kenya'
                else:
                    court.court_address = court.court_address

                if 'court_logo' in request.FILES:
                    court_logo = request.FILES['court_logo']
                    # Add your validation logic here
                    fs = FileSystemStorage()
                    filename = fs.save(court_logo.name, court_logo)
                    uploaded_file_url = fs.url(filename)
                    court.court_logo = uploaded_file_url
                elif not court.court_logo:
                    court.court_logo = None
                court.save()
                messages.success(request, 'Court updated successfully', extra_tags='toast')
                return redirect('admin-manage-court')
            else:
                messages.error(request, 'Court not found', extra_tags='toast')
                return redirect('admin-manage-court')


class AdminDeleteCourtView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.user_service = UserService()
        self.court_service = CourtService()

    def get(self, request, court_id):
        court = self.court_service.get_court_by_id(court_id)
        if court is not None:
            self.court_service.delete_court(court)
            messages.success(request, "Court Deleted Successfully.", extra_tags='toast')
            return redirect('admin-manage-court')
        else:
            messages.error(request, "Failed to delete this court.", extra_tags='toast')


class AdminManageJudgeView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        try:
            judges = self.user_service.get_user_by_role('judge')
        except:
            judges = None
            messages.error(request, 'No judges found in the database', extra_tags='toast')

        context = {
            'user_info': user_info,
            'judges': judges
        }

        return render(request, 'admin-manage-judge.html', context)


class AdminCreateJudgeView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration_service = RegistrationService(AdminService(), ClerkService())
        self.user_service = UserService()
        self.court_service = CourtService()
        self.user_service = UserService()

    def get(self, request):
        counties = self.user_service.get_counties()
        tribes = self.user_service.get_tribes()
        court_objects = self.court_service.get_all_courts()
        user = request.user
        user_info = self.user_service.get_user_info(user.username)

        # if no court in the database, redirect to create court with a message
        if len(court_objects) == 0:
            messages.error(request, 'No courts found in the database. Please create a court first', extra_tags='toast')
            return redirect('admin-create-court')
        else:
            try:
                judges = self.user_service.get_user_by_role('judge')
            except:
                clerks = None
                messages.error(request, 'No judges found in the database', extra_tags='toast')

            context = {
                'counties': counties,
                'tribes': tribes,
                'court_objects': court_objects,
                'user_info': user_info,
                'judges': judges
            }

            return render(request, 'admin-create-judge.html', context)

    def post(self, request):
        if request.method == 'POST':
            profile_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
            if profile_image is not None:
                fs = FileSystemStorage()
                filename = fs.save(profile_image.name, profile_image)
                uploaded_file_url = filename
            else:
                uploaded_file_url = None

            # Concatenate the address fields
            postal_code = request.POST.get('postal_code')
            town_city = request.POST.get('town_city')
            building_name = request.POST.get('building_name', '')
            floor_number = request.POST.get('floor_number', '')
            street_name = request.POST.get('street_name', '')

            # first check if the password and confirm password match
            if request.POST['password'] != request.POST['confirm_password']:
                messages.error(request, 'Password and confirm password do not match', extra_tags='toast')
                return render(request, 'register.html')
            else:
                # create user
                user = self.registration_service.register_user(

                    role=request.POST['role'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'] if 'last_name' in request.POST else None,
                    username=request.POST['username'],
                    email=request.POST['email'],
                    national_id=request.POST['national_id'],
                    county_of_residence=request.POST['county_of_residence'],
                    phone_number=request.POST['phone_number'],
                    gender=request.POST['gender'],
                    tribe=request.POST['tribe'],
                    date_of_birth=request.POST['date_of_birth'],
                    address=f'{postal_code}, {building_name}, {floor_number} Floor, {street_name}, {town_city}, Kenya',
                    password=make_password(request.POST['password']),
                    is_active=True,
                    is_staff=True,
                    is_superuser=False,
                    profile_image=uploaded_file_url
                )

            # assign user to court
            court_id = request.POST['courts']
            court = self.court_service.get_court_by_id(court_id)
            self.user_service.assign_user_to_court(user, court)

            if not user.is_approved:
                messages.success(request, 'The Judge has been created successfully. Please approve their account',
                                 extra_tags='toast')
                return redirect('admin-manage-judge')
            else:
                messages.success(request, 'The Judge has been created successfully. The Judge can now login',
                                 extra_tags='toast')
                return redirect('admin-manage-judge')

        return render(request, 'admin-create-clerk.html')


class AdminEditJudgeView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration_service = RegistrationService(AdminService(), ClerkService())
        self.user_service = UserService()
        self.court_service = CourtService()

    def get(self, request, user_id):
        counties = self.user_service.get_counties()
        tribes = self.user_service.get_tribes()
        court_objects = self.court_service.get_all_courts()
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        try:
            judge = self.user_service.get_user_by_id(user_id)
        except UserDoesNotExist:
            messages.error(request, 'Judge not found', extra_tags='toast')
            return redirect('admin-manage-judge')

        context = {
            'counties': counties,
            'user_info': user_info,
            'judge': judge,
            'tribes': tribes,
            'court_objects': court_objects,

        }

        return render(request, 'admin-edit-judge.html', context)

    def post(self, request, user_id):
        # check which values have been passed, if they are not empty, update those fields and leave the rest unchanged
        if request.method == 'POST':
            judge = self.user_service.get_user_by_id(user_id)

            # Concatenate the address fields and set the new values and if not exist retain old ones
            postal_code = request.POST.get('postal_code', '')
            town_city = request.POST.get('town_city', '')
            building_name = request.POST.get('building_name', '')
            floor_number = request.POST.get('floor_number', '')
            street_name = request.POST.get('street_name', '')

            if judge is not None:

                judge.first_name = request.POST.get('first_name', judge.first_name)
                judge.last_name = request.POST.get('last_name', judge.last_name)
                judge.username = request.POST.get('username', judge.username)
                judge.email = request.POST.get('email', judge.email)
                judge.national_id = request.POST.get('national_id', judge.national_id)
                judge.county_of_residence = request.POST.get('county_of_residence', judge.county_of_residence)
                judge.phone_number = request.POST.get('phone_number', judge.phone_number)
                judge.gender = request.POST.get('gender', judge.gender)
                judge.tribe = request.POST.get('tribe', judge.tribe)
                judge.date_of_birth = request.POST.get('date_of_birth', judge.date_of_birth)
                # use the old address if new one not provided
                if postal_code != '' and town_city != '' and building_name != '' and floor_number != '' and street_name != '':
                    judge.address = f'{postal_code}, {building_name}, {floor_number} Floor, {street_name}, {town_city}, Kenya'
                else:
                    judge.address = judge.address

                judge.password = make_password(request.POST.get('password', None))
                if 'profile_image' in request.FILES:
                    profile_image = request.FILES['profile_image']
                    # Add your validation logic here
                    fs = FileSystemStorage()
                    filename = fs.save(profile_image.name, profile_image)
                    uploaded_file_url = fs.url(filename)
                    judge.profile_image = uploaded_file_url
                elif not judge.profile_image:
                    judge.profile_image = None
                judge.save()
                messages.success(request, 'Judge updated successfully', extra_tags='toast')
                return redirect('admin-manage-judge')
            else:
                messages.error(request, 'Judge not found', extra_tags='toast')
                return redirect('admin-manage-judge')


class AdminDeleteJudgeView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.user_service = UserService()

    def get(self, request, user_id):
        user = self.user_service.get_user_by_id(user_id)
        if user is not None:
            self.user_service.delete_user(user)
            messages.success(request, 'Judge deleted successfully', extra_tags='toast')
        else:
            messages.error(request, 'Judge not found', extra_tags='toast')
        return redirect('admin-manage-judge')


class ManageProfileView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.court_service = CourtService()

    def get(self, request, user_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        roles = self.user_service.get_role_by_user(user)
        counties = self.user_service.get_counties()
        tribes = self.user_service.get_tribes()
        court_objects = self.court_service.get_all_courts()
        try:
            user = self.user_service.get_user_by_id(user_id)
        except UserDoesNotExist:
            messages.error(request, 'Account not found', extra_tags='toast')
            return redirect('dashboard')

        context = {
            'user_info': user_info,
            'user': user,
            'roles': roles,
            'counties': counties,
            'tribes': tribes,
            'court_objects': court_objects
        }

        return render(request, 'manage-profile.html', context)

    def post(self, request, user_id):
        if request.method == 'POST':
            user = self.user_service.get_user_by_id(user_id)

            # Concatenate the address fields and set the new values and if not exist retain old ones
            postal_code = request.POST.get('postal_code', '')
            town_city = request.POST.get('town_city', '')
            building_name = request.POST.get('building_name', '')
            floor_number = request.POST.get('floor_number', '')
            street_name = request.POST.get('street_name', '')

            if user is not None:
                user.first_name = request.POST.get('first_name', user.first_name)
                user.last_name = request.POST.get('last_name', user.last_name)
                user.username = request.POST.get('username', user.username)
                user.email = request.POST.get('email', user.email)
                user.national_id = request.POST.get('national_id', user.national_id)
                user.county_of_residence = request.POST.get('county_of_residence', user.county_of_residence)
                user.phone_number = request.POST.get('phone_number', user.phone_number)
                user.gender = request.POST.get('gender', user.gender)
                user.tribe = request.POST.get('tribe', user.tribe)
                user.date_of_birth = request.POST.get('date_of_birth', user.date_of_birth)
                # use the old address if new one not provided
                if postal_code != '' and town_city != '' and building_name != '' and floor_number != '' and street_name != '':
                    user.address = f'{postal_code}, {building_name}, {floor_number} Floor, {street_name}, {town_city}, Kenya'
                else:
                    user.address = user.address

                user.password = make_password(request.POST.get('password', None))
                profile_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
                if profile_image is not None:
                    # Add your validation logic here
                    fs = FileSystemStorage()
                    filename = fs.save(profile_image.name, profile_image)
                    uploaded_file_url = filename
                    user.profile_image = uploaded_file_url
                elif not user.profile_image:
                    user.profile_image = None
                user.save()
                messages.success(request, 'Your account has been updated successfully', extra_tags='toast')
                return redirect('dashboard')
            else:
                messages.error(request, 'We cannot find your account in our database. Maybe it got deleted?',
                               extra_tags='toast')
                return redirect('dashboard')


## Clerk Views
class ClerkManageParticipantView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.court_service = CourtService()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        court_objects = self.court_service.get_all_courts()

        try:
            roles = ['participant', 'lawyer', 'observer']
            participants = []
            for role in roles:
                participants.extend(self.user_service.get_user_by_role(role))
        except:
            participants = None
            messages.error(request, 'No users found in the database', extra_tags='toast')

        context = {
            'user_info': user_info,
            'participants': participants,
            'court_objects': court_objects,
        }

        return render(request, 'clerk-manage-participant.html', context)


class ClerkCreateParticipantView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.registration_service = RegistrationService(AdminService(), ClerkService())
        self.user_service = UserService()
        self.user_service = UserService()
        self.court_service = CourtService()

    def get(self, request):
        counties = self.user_service.get_counties()
        tribes = self.user_service.get_tribes()
        court_objects = self.court_service.get_all_courts()

        context = {
            'counties': counties,
            'tribes': tribes,
            'court_objects': court_objects
        }

        # if no court in the database, redirect to create court with a message
        if len(court_objects) == 0:
            messages.error(request, 'No courts found in the database. Please create a court first', extra_tags='toast')
            return redirect('admin-create-court')
        else:
            return render(request, 'clerk-create-participant.html', context)

    def post(self, request):
        if request.method == 'POST':
            profile_image = request.FILES['profile_image'] if 'profile_image' in request.FILES else None
            if profile_image is not None:
                fs = FileSystemStorage()
                filename = fs.save(profile_image.name, profile_image)
                uploaded_file_url = filename
            else:
                uploaded_file_url = None

            # Concatenate the address fields
            postal_code = request.POST.get('postal_code')
            town_city = request.POST.get('town_city')
            building_name = request.POST.get('building_name', '')
            floor_number = request.POST.get('floor_number', '')
            street_name = request.POST.get('street_name', '')

            # first check if the password and confirm password match
            if request.POST['password'] != request.POST['confirm_password']:
                messages.error(request, 'Password and confirm password do not match', extra_tags='toast')
                return render(request, 'clerk-create-participant.html')
            else:
                # create user
                user = self.registration_service.register_user(

                    role=request.POST['role'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'] if 'last_name' in request.POST else None,
                    username=request.POST['username'],
                    email=request.POST['email'],
                    national_id=request.POST['national_id'],
                    county_of_residence=request.POST['county_of_residence'],
                    phone_number=request.POST['phone_number'],
                    gender=request.POST['gender'],
                    tribe=request.POST['tribe'],
                    date_of_birth=request.POST['date_of_birth'],
                    address=f'{postal_code}, {building_name}, {floor_number} Floor, {street_name}, {town_city}, Kenya',
                    password=make_password(request.POST['password']),
                    is_active=True,
                    is_staff=False,
                    is_superuser=False,
                    profile_image=uploaded_file_url
                )

                # assign user to court
                court_id = request.POST['courts']
                court = self.court_service.get_court_by_id(court_id)
                self.user_service.assign_user_to_court(user, court)

            if not user.is_approved:
                messages.success(request, 'participant has been created successfully. Please wait for approval',
                                 extra_tags='toast')
                messages.warning(request, 'participant is pending approval', extra_tags='modal')
                return redirect('pending-approval')
            else:
                messages.success(request, 'participant has been created successfully. The participant can now login',
                                 extra_tags='toast')
                return redirect('clerk-manage-participant')

        return render(request, 'clerk-create-participant.html')


class ClerkApproveParticipantView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.user_service = UserService()
        self.court_service = CourtService()

    def get(self, request, user_id):
        user = self.user_service.get_user_by_id(user_id)
        if user is not None:
            user.is_approved = True
            user.save()
            messages.success(request, 'User approved successfully', extra_tags='toast')
        else:
            messages.error(request, 'User not found', extra_tags='toast')
        return redirect('clerk-manage-participant')


class ClerkDeleteParticipantView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.user_service = UserService()

    def get(self, request, user_id):
        user = self.user_service.get_user_by_id(user_id)
        if user is not None:
            self.user_service.delete_user(user)
            messages.success(request, 'User deleted successfully', extra_tags='toast')
        else:
            messages.error(request, 'User not found', extra_tags='toast')
        return redirect('clerk-manage-participant')


class ClerkManageCaseView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.case_service = CaseService()
        self.invoice_service = InvoiceService()
        self.case_proceeding_service = CaseProceedingService()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        cases = self.case_service.get_all_cases()

        for case in cases:
            case_proceedings = self.case_proceeding_service.get_case_proceeding_by_case(case)
            for case_proceeding in case_proceedings:
                if self.invoice_service.get_invoice_by_case_proceeding(
                        case_proceeding) is not None or case_proceeding.document is not None or case_proceeding.document.document_type in [
                    'judgement', 'opinion', 'verdict', 'sentence', 'decree', 'mandate, injuction', 'transcript']:
                    case.case_status = 'concluded'
                    case.save()
                elif self.invoice_service.get_invoice_by_case_proceeding(
                        case_proceeding) is None and case_proceeding.document is not None:
                    case.case_status = 'ongoing'
                    case.save()
                else:
                    case.case_status = 'pending'
                    case.save()

        context = {
            'user_info': user_info,
            'cases': cases,
        }

        return render(request, 'clerk-manage-case.html', context)


class ClerkCreateCaseView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.case_service = CaseService()
        self.court_service = CourtService()

    def get(self, request):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        court_objects = self.court_service.get_all_courts()
        plaintiffs = self.user_service.get_user_by_role('participant')
        defendants = self.user_service.get_user_by_role('participant')
        judges = self.user_service.get_user_by_role('judge')
        clerks = self.user_service.get_user_by_role('clerk')
        observers = self.user_service.get_user_by_role('participant')
        amicus = self.user_service.get_user_by_role('participant')
        lawyers = self.user_service.get_user_by_role('lawyer')
        decisions = self.case_service.get_decision()
        context = {
            'user_info': user_info,
            'court_objects': court_objects,
            'plaintiffs': plaintiffs,
            'defendants': defendants,
            'judges': judges,
            'clerks': clerks,
            'observers': observers,
            'amicus': amicus,
            'lawyers': lawyers,
            'decisions': decisions
        }

        return render(request, 'clerk-create-case.html', context)

    def post(self, request):
        if request.method == 'POST':
            # Retrieve the IDs from the form
            court_id = request.POST['court']

            # Retrieve the Court and User instances
            court = self.court_service.get_court_by_id(court_id)

            # Create the case
            case = self.case_service.create_case(
                case_name=request.POST['case_name'],
                case_type=request.POST['case_type'],
                court=court,  # Pass the Court instance
                case_description=request.POST['case_description'],
                case_status=request.POST['case_status'],
                date_filed=request.POST['date_filed'],
                date_hearing=request.POST['date_hearing'],
                relief_sought=request.POST['relief_sought'],
                decision=request.POST['decision'],
                created_by=request.user
            )

            # Retrieve the plaintiff and defendant IDs from the form
            plaintiff_ids = request.POST.getlist('plaintiffs')
            defendant_ids = request.POST.getlist('defendants')
            judge_ids = request.POST.getlist('judges')
            clerk_ids = request.POST.getlist('clerks')
            observer_ids = request.POST.getlist('observers')
            amicus_ids = request.POST.getlist('amicus')

            # Assign the plaintiffs and defendants to the case
            for plaintiff_id in plaintiff_ids:
                plaintiff = self.user_service.get_user_by_id(plaintiff_id)
                self.case_service.assign_user_to_case(case, plaintiff, 'plaintiff')

            for defendant_id in defendant_ids:
                defendant = self.user_service.get_user_by_id(defendant_id)
                self.case_service.assign_user_to_case(case, defendant, 'defendant')

            # Assign the judges and clerks to the case
            for judge_id in judge_ids:
                judge = self.user_service.get_user_by_id(judge_id)
                self.case_service.assign_user_to_case(case, judge, 'judge')

            for clerk_id in clerk_ids:
                clerk = self.user_service.get_user_by_id(clerk_id)
                self.case_service.assign_user_to_case(case, clerk, 'clerk')

            # Assign the observers and amicus to the case
            for observer_id in observer_ids:
                observer = self.user_service.get_user_by_id(observer_id)
                self.case_service.assign_user_to_case(case, observer, 'observer')

            for amicus_id in amicus_ids:
                amicus = self.user_service.get_user_by_id(amicus_id)
                self.case_service.assign_user_to_case(case, amicus, 'amicus')

            if case is not None:
                messages.success(request, 'Case created successfully', extra_tags='toast')
                return redirect('clerk-manage-case')
            else:
                messages.error(request, 'Failed to create case', extra_tags='toast')
                return render(request, 'clerk-create-case.html')


class ClerkEditCaseView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.case_service = CaseService()
        self.court_service = CourtService()

    def get(self, request, case_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        court_objects = self.court_service.get_all_courts()
        plaintiffs = self.user_service.get_user_by_role('participant')
        defendants = self.user_service.get_user_by_role('participant')
        case = self.case_service.get_case_by_id(case_id)
        decisions = self.case_service.get_decision()

        context = {
            'user_info': user_info,
            'court_objects': court_objects,
            'plaintiffs': plaintiffs,  # corrected here
            'defendants': defendants,
            'case': case,
            'decisions': decisions
        }

        return render(request, 'clerk-edit-case.html', context)

    def post(self, request, case_id):
        if request.method == 'POST':
            case = self.case_service.get_case_by_id(case_id)

            if case is not None:
                # Retrieve the IDs from the form
                court_id = request.POST['court']
                plaintiff_id = request.POST['plaintiff']
                defendant_id = request.POST['defendant']

                # Retrieve the Court and User instances
                court = self.court_service.get_court_by_id(court_id)
                plaintiff = self.user_service.get_user_by_id(plaintiff_id)
                defendant = self.user_service.get_user_by_id(defendant_id)

                # Update the case
                case.case_name = request.POST.get('case_name', case.case_name)
                case.case_type = request.POST.get('case_type', case.case_type)
                case.court = court  # Pass the Court instance
                case.case_description = request.POST.get('case_description', case.case_description)
                case.case_status = request.POST.get('case_status', case.case_status)
                case.date_filed = request.POST.get('date_filed', case.date_filed)
                case.date_hearing = request.POST.get('date_hearing', case.date_hearing)
                case.relief_sought = request.POST.get('relief_sought', case.relief_sought)
                case.decision = request.POST.get('decision', case.decision)
                case.plaintiff = plaintiff  # Pass the User instance
                case.defendant = defendant  # Pass the User instance
                case.save()

                messages.success(request, 'Case updated successfully', extra_tags='toast')
                return redirect('clerk-manage-case')
            else:
                messages.error(request, 'Case not found', extra_tags='toast')
                return redirect('clerk-manage-case')


class ClerkDeleteCaseView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_service = CaseService()

    def get(self, request, case_id):
        case = self.case_service.get_case_by_id(case_id)
        if case is not None:
            self.case_service.delete_case(case)
            messages.success(request, 'Case deleted successfully', extra_tags='toast')
        else:
            messages.error(request, 'Case not found', extra_tags='toast')
        return redirect('clerk-manage-case')


class ParticipantManageCaseView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_service = UserService()
        self.case_service = CaseService()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        cases = self.case_service.get_all_cases()

        context = {
            'user_info': user_info,
            'cases': cases
        }

        return render(request, 'participant-manage-case.html', context)


## Case Proceeding Views
class ManageCaseProceedingView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_proceeding_service = CaseProceedingService()
        self.user_service = UserService()
        self.case_service = CaseService()

    def get(self, request, case_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        case = self.case_service.get_case_by_id(case_id)
        if user_info.role == 'clerk' or user_info.role == 'judge':
            case_proceedings = self.case_proceeding_service.get_case_proceeding_by_case(case)
        elif user_info.role == 'participant' or user_info.role == 'lawyer':
            case_proceedings = self.case_proceeding_service.get_case_proceeding_by_case(case).exclude(
                confidentiality__in=['critical'])
        else:
            case_proceedings = self.case_proceeding_service.get_case_proceeding_by_case(case).exclude(
                confidentiality__in=['medium', 'high', 'critical'])

        context = {
            'user_info': user_info,
            'case': case,
            'case_proceedings': case_proceedings
        }

        return render(request, 'manage-case-proceeding.html', context)

    def post(self, request, case_id):
        pass


class CreateCaseProceedingView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_proceeding_service = CaseProceedingService()
        self.user_service = UserService()
        self.case_service = CaseService()

    def get(self, request, case_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        case = self.case_service.get_case_by_id(case_id)
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_case(case)
        document_types = self.case_proceeding_service.get_document_types_for_role(request.user.role)
        document_confidentialities = self.case_proceeding_service.get_document_confidentiality()
        participants = self.user_service.get_user_by_role('participant')
        verdicts = self.case_proceeding_service.get_verdicts()
        relief_types = self.case_proceeding_service.get_relief_types()
        form = CaseProceedingForm()
        context = {
            'user_info': user_info,
            'case': case,
            'case_proceeding': case_proceeding,
            'document_types': document_types,
            'document_confidentialities': document_confidentialities,
            'participants': participants,
            'verdicts': verdicts,
            'relief_types': relief_types,
            'form': form
        }
        return render(request, 'create-case-proceeding.html', context)

    def post(self, request, case_id):
        # Retrieve the case proceeding from the submitted CaseProceedingForm in forms.py
        form = CaseProceedingForm(request.POST, request.FILES)
        case = self.case_service.get_case_by_id(case_id)
        if form.is_valid():
            case_proceeding = form.save(commit=False)
            case_proceeding.filed_by = request.user
            case_proceeding.filed_as = request.user.role
            case_proceeding.case = case
            case_proceeding.save()

            # handle the html form fields
            document_name = request.POST.get('document_name')
            document_type = request.POST.get('document_type')
            document_confidentiality = request.POST.get('document_confidentiality')

            case_proceeding.document_name = document_name
            case_proceeding.document_type = document_type
            case_proceeding.confidentiality = document_confidentiality
            case_proceeding.save()



            # Handle reliefs
            for i in range(1, 9):  # Iterate over numbers from 1 to 8
                participant_id = request.POST.get(f'participant_{i}')
                verdict = request.POST.get(f'verdict_{i}')
                case.decision = verdict
                case.save()
                relief_type = request.POST.get(f'relief_type_{i}')
                value = request.POST.get(f'value_{i}')

                if participant_id and verdict and relief_type and value:  # Check if the relief data exists
                    participant = self.user_service.get_user_by_id(participant_id)
                    relief = self.case_proceeding_service.create_relief(participant, case_proceeding,
                                                                        case_proceeding.case.court, relief_type,
                                                                        verdict, value)
                    case_proceeding.reliefs.add(relief)

            messages.success(request, 'Case proceeding updated successfully', extra_tags='toast')
            return redirect('manage-case-proceeding', case_id=case_proceeding.case.id)
        else:
            messages.error(request, 'Invalid form', extra_tags='toast')
            return redirect('manage-case-proceeding', case_id=case.id)


class ViewCaseProceedingView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_proceeding_service = CaseProceedingService()
        self.user_service = UserService()
        self.case_service = CaseService()

    def get(self, request, case_proceeding_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(case_proceeding_id)

        context = {
            'user_info': user_info,
            'case_proceeding': case_proceeding
        }

        return render(request, 'view-case-proceeding.html', context)


class EditCaseProceedingView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_proceeding_service = CaseProceedingService()
        self.user_service = UserService()
        self.case_service = CaseService()

    def get(self, request, case_proceeding_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(case_proceeding_id)
        document_types = self.case_proceeding_service.get_document_types_for_role(request.user.role)
        document_confidentialities = self.case_proceeding_service.get_document_confidentiality()
        participants = self.user_service.get_user_by_role('participant')
        verdicts = self.case_proceeding_service.get_verdicts()
        relief_types = self.case_proceeding_service.get_relief_types()
        form = CaseProceedingForm(instance=case_proceeding)
        relief_objects = case_proceeding.reliefs.all()
        context = {
            'user_info': user_info,
            'case_proceeding': case_proceeding,
            'document_types': document_types,
            'document_confidentialities': document_confidentialities,
            'participants': participants,
            'verdicts': verdicts,
            'relief_types': relief_types,
            'relief_objects': relief_objects,
            'form': form
        }

        return render(request, 'edit-case-proceeding.html', context)

    def post(self, request, case_proceeding_id):
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(case_proceeding_id)
        form = CaseProceedingForm(request.POST, request.FILES, instance=case_proceeding)
        if form.is_valid():
            case_proceeding = form.save(commit=False)
            case_proceeding.filed_by = request.user
            case_proceeding.filed_as = request.user.role
            case_proceeding.save()

            # handle the html form fields
            document_name = request.POST.get('document_name')
            document_type = request.POST.get('document_type')
            document_confidentiality = request.POST.get('document_confidentiality')

            case_proceeding.document_name = document_name
            case_proceeding.document_type = document_type
            case_proceeding.confidentiality = document_confidentiality
            case_proceeding.save()

            # Handle reliefs
            for i in range(1, 9):  # Iterate over numbers from 1 to 8
                participant_id = request.POST.get(f'participant_{i}')
                verdict = request.POST.get(f'verdict_{i}')
                relief_type = request.POST.get(f'relief_type_{i}')
                value = request.POST.get(f'value_{i}')

                if participant_id and verdict and relief_type and value:  # Check if the relief data exists
                    participant = self.user_service.get_user_by_id(participant_id)
                    relief = self.case_proceeding_service.create_relief(participant, case_proceeding,
                                                                        case_proceeding.case.court, relief_type,
                                                                        verdict,
                                                                        value)
                    case_proceeding.reliefs.add(relief)
            messages.success(request, 'Case proceeding updated successfully', extra_tags='toast')
            return redirect('manage-case-proceeding', case_id=case_proceeding.case.id)
        else:
            messages.error(request, 'Invalid form', extra_tags='toast')
            return redirect('manage-case-proceeding', case_id=case_proceeding.case.id)


class DeleteCaseProceedingView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_proceeding_service = CaseProceedingService()

    def get(self, request, case_proceeding_id):
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(case_proceeding_id)
        if case_proceeding is not None:
            self.case_proceeding_service.delete_case_proceeding(case_proceeding.id)
            messages.success(request, 'Case proceeding deleted successfully', extra_tags='toast')
        else:
            messages.error(request, 'Case proceeding not found', extra_tags='toast')
        return redirect('manage-case-proceeding', case_id=case_proceeding.case.id)


class DownloadCaseProceedingDocumentView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_proceeding_service = CaseProceedingService()

    def get(self, request, case_proceeding_id):
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(case_proceeding_id)
        if case_proceeding is not None:
            # Create a file-like buffer to receive PDF data.
            buffer = BytesIO()

            # Create the PDF object, using the buffer as its "file."
            pisa_status = pisa.CreatePDF(case_proceeding.content, dest=buffer)

            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            buffer.seek(0)

            return FileResponse(buffer, as_attachment=True, filename=f'{case_proceeding.document_name}.pdf')

        else:
            messages.error(request, 'Case proceeding not found', extra_tags='toast')
            return redirect('manage-case-proceeding', case_id=case_proceeding.case.id)


## Invoice Views
class ManageInvoiceView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice_service = InvoiceService()
        self.user_service = UserService()
        self.payment_service = PaymentService()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        user_info = self.user_service.get_user_info(user.username)

        # each signed-in user should only see their invoices except for the clerk
        # the participants in the invoice should be checked against the logged in user, if any of the participants is logged in user, the invoice should be displayed
        if user_info.role == 'clerk':
            invoices = self.invoice_service.get_all_invoices()
        else:
            invoices = self.invoice_service.get_invoice_by_participant(user)
        payments = self.payment_service.get_all_payments()

        for payment in payments:
            if payment.invoice is not None:
                invoice = self.invoice_service.get_invoice_by_id(payment.invoice.id)
                invoice.invoice_status = 'paid'
                invoice.save()
            elif payment.payment_status == 'cancelled':
                payment.invoice.invoice_status = 'cancelled'
                payment.invoice.save()

        # check if the invoice is overdue and the status does not qualify for paid
        for invoice in invoices:
            if invoice.invoice_due_date < datetime.now().date() and invoice.invoice_status != 'paid':
                invoice.invoice_status = 'overdue'
                invoice.save()
            elif invoice.invoice_due_date > datetime.now().date() and invoice.invoice_status != 'paid':
                invoice.invoice_status = 'pending'
                invoice.save()
            else:
                invoice.invoice_status = 'paid'
                invoice.save()

        # add a 16% tax on all invoice amounts
        for invoice in invoices:
            invoice.invoice_amount = math.ceil(invoice.invoice_amount * 1.16)
            invoice.invoice_amount = float(invoice.invoice_amount)
            invoice.invoice_amount = "{:.2f}".format(invoice.invoice_amount)

        context = {
            'user_info': user_info,
            'invoices': invoices,
            'payments': payments
        }

        return render(request, 'manage-invoice.html', context)


class SelectParticipantForInvoiceView(View):
    # 1. get the participants from case_proceeding.case.participants
    # 2. filter them by the participants in the case_proceeding.reliefs.participants
    # 3. return the filtered participants and pass them to the form
    # 4. note that the format 'case_proceeding.case.participants' and 'case_proceeding.reliefs.participants' is a format not an actual code use it for reference only
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.case_proceeding_service = CaseProceedingService()
        self.user_service = UserService()

    def get(self, request, case_proceeding_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(case_proceeding_id)
        participants = (self.user_service.get_user_by_role('participant').filter(
            id__in=case_proceeding.reliefs.values_list('participant', flat=True)))
        context = {
            'user_info': user_info,
            'case_proceeding': case_proceeding,
            'participants': participants,
        }
        return render(request, 'select-participant-for-invoice.html', context)

    def post(self, request, case_proceeding_id):
        # 1. once you receive the participant of choice, pass the participant and their relief and the
        # case_proceeding to the class CreateInvoiceView
        participant_id = request.POST.get('participant')
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(case_proceeding_id)
        participant = self.user_service.get_user_by_id(participant_id)

        if participant is not None:
            messages.success(request,
                             f'Participant {participant.first_name} {participant.last_name} selected successfully',
                             extra_tags='toast')
            return redirect('create-invoice', case_proceeding_id=case_proceeding_id, participant_id=participant_id)
        else:
            messages.error(request, 'Participant not found', extra_tags='toast')
            return redirect('manage-invoice')


class CreateInvoiceView(View):
    # 1. having received the participant and their relief and the case_proceeding, create variables for the participant and their relief and the case_proceeding
    # 2. create a form for the invoice and pass the participant and their relief and the case_proceeding to the form
    # 3. save the form and create the invoice
    # 4. display the invoice using view-invoice view
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice_service = InvoiceService()
        self.user_service = UserService()
        self.case_proceeding_service = CaseProceedingService()

    def get(self, request, case_proceeding_id, participant_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        participants = self.user_service.get_user_by_id(participant_id)
        invoice_types = self.invoice_service.get_invoice_types()
        invoice_status_objects = self.invoice_service.get_invoice_status()
        invoice_amount = self.case_proceeding_service.get_relief_by_participant(participants,
                                                                                case_proceeding_id).first().value
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(case_proceeding_id)
        context = {
            'user_info': user_info,
            'case_proceeding': case_proceeding,
            'participants': participants,
            'invoice_types': invoice_types,
            'invoice_status_objects': invoice_status_objects,
            'invoice_amount': invoice_amount
        }
        return render(request, 'create-invoice.html', context)

    def post(self, request, case_proceeding_id, participant_id):

        # convert participant_id to the coresponding participant object from the database
        participant = self.user_service.get_user_by_id(participant_id)

        # retrieve the CaseProceeding object that corresponds to case_proceeding_id
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(case_proceeding_id)

        # create the invoice
        invoice = self.invoice_service.create_invoice(
            invoice_type=request.POST.get('invoice_type'),
            invoice_status=request.POST.get('invoice_status'),
            invoice_amount=request.POST.get('invoice_amount'),
            participant=participant,
            invoice_due_date=request.POST.get('invoice_due_date'),
            case_proceeding=case_proceeding,
            created_by=request.user,
            relieved_by=case_proceeding.reliefs.filter(participant=participant).first()
        )

        if invoice is not None:
            messages.success(request, 'Invoice created successfully', extra_tags='toast')
            return redirect('view-invoice', invoice.id)
        else:
            messages.error(request, 'Failed to create invoice', extra_tags='toast')
            return redirect('manage-invoice')


class EditInvoiceView(View):
    # 1. get the invoice by id
    # 2. pass the invoice
    # 3. save the form and update the invoice
    # 4. display the invoice using view-invoice view
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice_service = InvoiceService()
        self.user_service = UserService()

    def get(self, request, invoice_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        invoice_types = self.invoice_service.get_invoice_types()
        invoice_status_objects = self.invoice_service.get_invoice_status()
        context = {
            'user_info': user_info,
            'invoice': invoice,
            'invoice_types': invoice_types,
            'invoice_status_objects': invoice_status_objects
        }
        return render(request, 'edit-invoice.html', context)

    def post(self, request, invoice_id):
        # use html form
        invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        invoice.invoice_type = request.POST.get('invoice_type')
        invoice.invoice_status = request.POST.get('invoice_status')
        invoice.invoice_amount = request.POST.get('invoice_amount')
        invoice.invoice_due_date = request.POST.get('invoice_due_date')
        invoice.save()
        if invoice is not None:
            messages.success(request, 'Invoice updated successfully', extra_tags='toast')
            return redirect('view-invoice', invoice.id)
        else:
            messages.error(request, 'Failed to update invoice', extra_tags='toast')
            return redirect('manage-invoice')


class DeleteInvoiceView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice_service = InvoiceService()

    def get(self, request, invoice_id):
        invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        if invoice is not None:
            self.invoice_service.delete_invoice(invoice)
            messages.success(request, 'Invoice deleted successfully', extra_tags='toast')
        else:
            messages.error(request, 'Invoice not found', extra_tags='toast')
        return redirect('manage-invoice')


class ViewInvoiceView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice_service = InvoiceService()
        self.user_service = UserService()
        self.case_proceeding_service = CaseProceedingService()
        self.case = CaseService()

    def get(self, request, invoice_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(invoice.case_proceeding.id)
        case = self.case.get_case_by_id(case_proceeding.case.id)
        court = case.court
        verdict = self.case_proceeding_service.get_relief_by_case_proceeding(case_proceeding).first().verdict
        # calculate the tax and total amount
        tax = invoice.invoice_amount * 0.16
        grand_total = invoice.invoice_amount * 1.16
        # convert the grand total to an integer.
        grand_total = math.ceil(grand_total)

        # Format the numbers with commas as thousand separators
        invoice.invoice_amount = "{:,}".format(invoice.invoice_amount)
        tax = "{:,}".format(tax)
        grand_total = "{:,}".format(grand_total)

        context = {
            'user_info': user_info,
            'invoice': invoice,
            'case_proceeding': case_proceeding,
            'case': case,
            'court': court,
            'tax': tax,
            'grand_total': grand_total,
            'verdict': verdict
        }
        return render(request, 'view-invoice.html', context)


class DownloadInvoiceView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.invoice_service = InvoiceService()
        self.user_service = UserService()
        self.case_proceeding_service = CaseProceedingService()
        self.case = CaseService()

    def get(self, request, invoice_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(invoice.case_proceeding.id)
        case = self.case.get_case_by_id(case_proceeding.case.id)
        court = case.court
        verdict = self.case_proceeding_service.get_relief_by_case_proceeding(case_proceeding).first().verdict
        tax = invoice.invoice_amount * 0.16
        grand_total = invoice.invoice_amount * 1.16

        grand_total = invoice.invoice_amount * 1.16
        # convert the grand total to an integer.
        grand_total = math.ceil(grand_total)

        invoice.invoice_amount = "{:,}".format(invoice.invoice_amount)
        tax = "{:,}".format(tax)
        grand_total = "{:,}".format(grand_total)

        # Fetch the logo image path
        court_logo_path = court.court_logo.path if court.court_logo else None

        context = {
            'user_info': user_info,
            'invoice': invoice,
            'case_proceeding': case_proceeding,
            'case': case,
            'court': court,
            'tax': tax,
            'grand_total': grand_total,
            'verdict': verdict,
            'court_logo_path': court_logo_path,
        }

        # Render the template with context data
        template = get_template('view-invoice.html')
        html = template.render(context)

        # Create a file-like buffer to receive PDF data
        buffer = BytesIO()

        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=buffer)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        # Set response content type
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Invoice #{invoice.invoice_id}.pdf"'

        # Close the buffer and return the response
        buffer.close()
        return response


# Payment Views
class ManagePaymentView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_service = PaymentService()
        self.user_service = UserService()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        # each signed-in user should only see their payment except for the clerk
        if user_info.role == 'clerk':
            payments = self.payment_service.get_all_payments()
        else:
            payments = self.payment_service.get_payment_by_participant(user)

        for payment in payments:
            # convert the base 10 (eg. 2.0) to a float of 2dp (eg. 2.00)
            payment.amount = float(payment.amount)
            payment.amount = "{:.2f}".format(payment.amount)

        context = {
            'user_info': user_info,
            'payments': payments
        }
        return render(request, 'manage-payment.html', context)


class CreatePaymentView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_service = PaymentService()
        self.user_service = UserService()
        self.invoice_service = InvoiceService()
        self.payment_queue_service = PaymentQueueService()

    def get(self, request, invoice_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        invoice_no = self.invoice_service.get_invoice_by_id(invoice_id).invoice_id
        invoice_amount = self.invoice_service.get_invoice_by_id(invoice_id).invoice_amount
        # take the invoice amount as a float, add a 0.16 tax and convert it to an integer
        invoice_amount = math.ceil(invoice_amount * 1.16)
        defendant_name = user_info.first_name.upper() + ' ' + user_info.last_name.upper()
        defendant_phone = user_info.phone_number
        invoice_date = self.invoice_service.get_invoice_by_id(invoice_id).invoice_date
        account_reference = f'{invoice_no}'
        description = f'Payment of {invoice_no} for the judgement against {defendant_name} on {invoice_date}.'
        invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        context = {
            'user_info': user_info,
            'invoice_amount': invoice_amount,
            'invoice_no': invoice_no,
            'defendant_name': defendant_name,
            'defendant_phone': defendant_phone,
            'invoice_date': invoice_date,
            'account_reference': account_reference,
            'description': description,
            'invoice': invoice
        }
        return render(request, 'create-payment.html', context)

    def post(self, request, invoice_id):
        invoice = self.invoice_service.get_invoice_by_id(invoice_id)
        defendant_phone = request.POST.get('defendant_phone')
        defendant_name = request.POST.get('defendant_name')
        formatted_phone_number = ''.join(e for e in defendant_phone if e.isalnum())
        # remove the 0 and add 254
        formatted_phone_number = '254' + formatted_phone_number[1:]
        invoice_amount = request.POST.get('invoice_amount')
        formatted_invoice_amount = int(invoice_amount.replace(',', ''))
        account_reference = request.POST.get('account_reference')
        transaction_description = request.POST.get('description')

        # initiate mpesa stk_push
        mpesa_client = MpesaClient()
        phone_number = formatted_phone_number
        amount = formatted_invoice_amount
        account_reference = account_reference
        transaction_desc = transaction_description
        callback_url = 'https://courtixsoftware.pythonanywhere.com/callback/'
        response = mpesa_client.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)

        parsed_response = response.json()

        if parsed_response.get('ResponseCode') == '0':
            self.payment_queue_service.create_payment_queue(
                checkout_request_id=parsed_response['CheckoutRequestID'],
                phone_number=phone_number,
                amount=amount,
                account_reference=account_reference,
                transaction_description=transaction_desc,
                status='complete',
                invoice=invoice
            )
            messages.success(request, 'Please Enter your MPESA pin to complete your transaction', extra_tags='toast')
            return redirect('manage-payment')
        else:
            messages.error(request, 'Failed to initiate payment', extra_tags='toast')
        return redirect('manage-invoice')


logger = logging.getLogger(__name__)


@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_queue_service = PaymentQueueService()
        self.payment_service = PaymentService()
        self.invoice_service = InvoiceService()

    def parse_data(self, data):
        try:
            callback_data = data['Body']['stkCallback']
            checkout_request_id = callback_data['CheckoutRequestID']
            result_code = callback_data['ResultCode']
            result_desc = callback_data['ResultDesc']
            metadata = callback_data.get('CallbackMetadata', {}).get('Item', [])

            callback_details = {item['Name']: item.get('Value') for item in metadata}
            amount = callback_details.get('Amount')
            mpesa_receipt_number = callback_details.get('MpesaReceiptNumber')
            transaction_date = callback_details.get('TransactionDate')
            phone_number = callback_details.get('PhoneNumber')

            return {
                'checkout_request_id': checkout_request_id,
                'result_code': result_code,
                'result_desc': result_desc,
                'amount': amount,
                'mpesa_receipt_number': mpesa_receipt_number,
                'transaction_date': transaction_date,
                'phone_number': phone_number,
            }
        except KeyError as e:
            logger.error("Key error: %s", str(e))
            return None

    def handle_callback(self, data):
        details = self.parse_data(data)
        if not details:
            return HttpResponse('Bad Request: Invalid data', status=400)

        checkout_request_id = details['checkout_request_id']
        result_code = details['result_code']
        result_desc = details['result_desc']
        amount = details['amount']
        mpesa_receipt_number = details['mpesa_receipt_number']
        transaction_date = details['transaction_date']
        phone_number = details['phone_number']

        if result_code == 0:
            payment_queue = self.payment_queue_service.get_payment_queue_by_checkout_request_id(checkout_request_id)
            if not payment_queue:
                logger.error("No payment queue found for checkout_request_id: %s", checkout_request_id)
                return HttpResponse('Internal Server Error', status=500)

            invoice = payment_queue.invoice
            if not invoice:
                logger.error("No invoice found in payment queue for checkout_request_id: %s", checkout_request_id)
                return HttpResponse('Internal Server Error', status=500)

            if not invoice.participant:
                logger.error("No participant associated with the invoice for checkout_request_id: %s",
                             checkout_request_id)
                return HttpResponse('Internal Server Error', status=500)

            transaction = self.payment_service.create_payment(
                phone_number=phone_number,
                checkout_request_id=checkout_request_id,
                mpesa_reference=mpesa_receipt_number,
                description=payment_queue.transaction_description,
                amount=amount,
                status=1,
                participant=invoice.participant,  # Ensure participant is assigned correctly
                paid_for=f'{invoice.participant.first_name} {invoice.participant.last_name}',
                invoice=invoice
            )

            payment_queue.transaction = transaction
            payment_queue.save()
            messages.success(request, 'Payment received successfully', extra_tags='toast')
            return HttpResponse('Payment received successfully')
        else:
            payment_queue = self.payment_queue_service.get_payment_queue_by_checkout_request_id(checkout_request_id)
            payment_queue.status = 'failed'
            payment_queue.save()
            messages.error(request, 'Payment failed', extra_tags='toast')
            return HttpResponse('Payment failed')

    def post(self, request):
        try:
            raw_body = request.body.decode('utf-8')
            logger.info("Raw MPESA Callback data received: %s", raw_body)

            if not raw_body:
                logger.error("Empty body received in MPESA callback")
                return HttpResponse('Bad Request: Empty body', status=400)

            try:
                data = json.loads(raw_body)
            except json.JSONDecodeError as e:
                logger.error("JSON decode error: %s", str(e))
                return HttpResponse('Bad Request: Invalid JSON', status=400)

            return self.handle_callback(data)
        except Exception as e:
            logger.error("Error processing MPESA callback: %s", str(e))
            return HttpResponse('Internal Server Error', status=500)


class ViewPaymentReceiptView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_service = PaymentService()
        self.invoice_service = InvoiceService()
        self.user_service = UserService()
        self.case_proceeding_service = CaseProceedingService()
        self.case = CaseService()

    def get(self, request, payment_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        invoice = self.payment_service.get_payment_by_id(payment_id).invoice
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(invoice.case_proceeding.id)
        case = self.case.get_case_by_id(case_proceeding.case.id)
        court = case.court
        # calculate the tax and total amount
        payment = self.payment_service.get_payment_by_id(payment_id)
        tax_due = math.ceil(float(invoice.invoice_amount) * 0.16)
        tax_paid = float(payment.amount) - float(invoice.invoice_amount)
        tax_balance = tax_due - tax_paid
        amount_paid = (float(payment.amount) - math.ceil(tax_due))
        verdict = self.case_proceeding_service.get_relief_by_case_proceeding(case_proceeding).first().verdict
        balance = ((float(payment.amount) - math.ceil(tax_due)) - float(invoice.invoice_amount))
        total_due = float(invoice.invoice_amount) + tax_due
        total_paid = float(payment.amount)
        total_balance = total_due - total_paid

        # Format the numbers with commas as thousand separators and 2 decimal places
        formatted_invoice_amount = "{:,.2f}".format(invoice.invoice_amount)
        formatted_tax_due = "{:,.2f}".format(tax_due)
        formatted_tax_paid = "{:,.2f}".format(tax_paid)
        formatted_amount_paid = "{:,.2f}".format(amount_paid)
        formatted_tax_balance = "{:,.2f}".format(tax_balance)
        formatted_total_due = "{:,.2f}".format(total_due)
        formatted_total_paid = "{:,.2f}".format(total_paid)
        formatted_total_balance = "{:,.2f}".format(total_balance)
        formatted_balance = "{:,.2f}".format(balance)
        context = {
            'user_info': user_info,
            'payment': payment,
            'invoice': invoice,
            'case_proceeding': case_proceeding,
            'case': case,
            'court': court,
            'tax_due': formatted_tax_due,
            'tax_paid': formatted_tax_paid,
            'amount_paid': formatted_amount_paid,
            'invoice_amount': formatted_invoice_amount,
            'tax_balance': formatted_tax_balance,
            'verdict': verdict,
            'balance': formatted_balance,
            'total_due': formatted_total_due,
            'total_paid': formatted_total_paid,
            'total_balance': formatted_total_balance
        }
        return render(request, 'view-payment-receipt.html', context)


class DownloadPaymentReceiptView(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.payment_service = PaymentService()
        self.invoice_service = InvoiceService()
        self.user_service = UserService()
        self.case_proceeding_service = CaseProceedingService()
        self.case = CaseService()

    def get(self, request, payment_id):
        user = request.user
        user_info = self.user_service.get_user_info(user.username)
        invoice = self.payment_service.get_payment_by_id(payment_id).invoice
        case_proceeding = self.case_proceeding_service.get_case_proceeding_by_id(invoice.case_proceeding.id)
        case = self.case.get_case_by_id(case_proceeding.case.id)
        court = case.court
        # calculate the tax and total amount
        payment = self.payment_service.get_payment_by_id(payment_id)
        tax_due = math.ceil(float(invoice.invoice_amount) * 0.16)
        tax_paid = float(payment.amount) - float(invoice.invoice_amount)
        tax_balance = tax_due - tax_paid
        amount_paid = (float(payment.amount) - math.ceil(tax_due))
        verdict = self.case_proceeding_service.get_relief_by_case_proceeding(case_proceeding).first().verdict
        balance = ((float(payment.amount) - math.ceil(tax_due)) - float(invoice.invoice_amount))
        total_due = float(invoice.invoice_amount) + tax_due
        total_paid = float(payment.amount)
        total_balance = total_due - total_paid

        # Format the numbers with commas as thousand separators and 2 decimal places
        formatted_invoice_amount = "{:,.2f}".format(invoice.invoice_amount)
        formatted_tax_due = "{:,.2f}".format(tax_due)
        formatted_tax_paid = "{:,.2f}".format(tax_paid)
        formatted_amount_paid = "{:,.2f}".format(amount_paid)
        formatted_tax_balance = "{:,.2f}".format(tax_balance)
        formatted_total_due = "{:,.2f}".format(total_due)
        formatted_total_paid = "{:,.2f}".format(total_paid)
        formatted_total_balance = "{:,.2f}".format(total_balance)
        formatted_balance = "{:,.2f}".format(balance)

        # Fetch the logo image path
        court_logo_path = court.court_logo.path if court.court_logo else None

        context = {
            'user_info': user_info,
            'payment': payment,
            'invoice': invoice,
            'case_proceeding': case_proceeding,
            'case': case,
            'court': court,
            'tax_due': formatted_tax_due,
            'tax_paid': formatted_tax_paid,
            'amount_paid': formatted_amount_paid,
            'invoice_amount': formatted_invoice_amount,
            'tax_balance': formatted_tax_balance,
            'verdict': verdict,
            'balance': formatted_balance,
            'total_due': formatted_total_due,
            'total_paid': formatted_total_paid,
            'total_balance': formatted_total_balance,
            'court_logo_path': court_logo_path,
        }

        # Render the template with context data
        template = get_template('view-payment-receipt.html')
        html = template.render(context)

        # Create a file-like buffer to receive PDF data
        buffer = BytesIO()

        # Generate PDF
        pisa_status = pisa.CreatePDF(html, dest=buffer)

        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        # Set response content type
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Receipt #{payment.receipt_id}.pdf"'

        # Close the buffer and return the response
        buffer.close()
        return response

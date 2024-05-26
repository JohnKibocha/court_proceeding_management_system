from django.contrib import admin

from court_proceedings_management_application.models import User, Contact, Court, Case, CaseProceeding, Relief, Invoice, \
    Transaction, PaymentQueue


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'username', 'first_name', 'last_name', 'email', 'role', 'county_of_residence',
                    'date_joined',
                    'is_staff', 'is_active', 'is_superuser', 'is_approved', 'profile_image']
    list_filter = ['role', 'county_of_residence']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'role', 'county_of_residence']
    list_per_page = 20
    ordering = ['username', 'email', 'first_name', 'last_name', 'role', 'county_of_residence']
    fieldsets = (
        ('Personal Information', {
            'fields': ['user_id', 'profile_image', 'first_name', 'last_name', 'username', 'email', 'role',
                       'national_id',
                       'county_of_residence', 'phone_number', 'gender', 'date_of_birth', 'tribe', 'address']}),

        ('Relationships', {'fields': ['courts']}),

        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser', 'is_approved']})
    )


admin.site.register(User, UserAdmin)


class CourtAdmin(admin.ModelAdmin):
    list_display = ['court_id', 'name', 'court_logo', 'court_email', 'court_phone', 'court_address', 'location',
                    'court_type', 'created_by', 'created_on']
    list_filter = ['location', 'court_type']
    search_fields = ['name', 'location', 'court_type', 'created_by__username']
    list_per_page = 20
    ordering = ['name', 'location', 'court_type', 'created_by__username']

    fieldsets = [
        ('Court Information',
         {'fields': ['court_id', 'name', 'court_logo', 'court_email', 'court_phone', 'court_address', 'location',
                     'court_type']}),
        ('Metadata', {'fields': ['created_by']}),
    ]


admin.site.register(Court, CourtAdmin)


class CaseAdmin(admin.ModelAdmin):
    list_display = ['case_id', 'case_name', 'case_type', 'case_status', 'date_filed', 'date_hearing', 'court',
                    'created_by', 'created_on']
    list_filter = ['case_type', 'case_status', 'court', 'created_by']
    search_fields = ['case_name', 'case_type', 'case_status', 'court__name', 'created_by__username']
    list_per_page = 20
    ordering = ['case_name', 'case_type', 'case_status', 'court__name', 'created_by__username']
    fieldsets = [
        ('Case Information', {
            'fields': ['case_id', 'case_name', 'case_type', 'case_status', 'case_description', 'date_filed',
                       'plaintiffs', 'defendants', 'judges', 'clerks', 'observers', 'lawyers', 'amicus', 'date_hearing',
                       'court', 'relief_sought', 'decision']}),
        ('Metadata', {'fields': ['created_by']}),

    ]


admin.site.register(Case, CaseAdmin)


class CaseProceedingAdmin(admin.ModelAdmin):
    list_display = ['document_id', 'document_name', 'document_type', 'filed_by', 'filed_as', 'filed_on',
                    'confidentiality']
    list_filter = ['document_type', 'filed_by', 'filed_as', 'confidentiality', 'case']
    search_fields = ['document_name', 'document_type', 'filed_by__username', 'filed_as', 'case__case_name']
    list_per_page = 20
    ordering = ['document_name', 'document_type', 'filed_by__username', 'filed_as', 'case__case_name']
    fieldsets = [
        ('Document Information', {
            'fields': ['document_id', 'document_name', 'document_type', 'filed_by', 'filed_as', 'confidentiality',
                       'case', 'editors', 'content', 'reliefs']}),
    ]


admin.site.register(CaseProceeding, CaseProceedingAdmin)


class ReliefAdmin(admin.ModelAdmin):
    list_display = ['participant', 'court', 'relief_type', 'verdict', 'value']
    list_filter = ['participant', 'court', 'relief_type', 'verdict']
    search_fields = ['participant__username', 'court__name', 'relief_type', 'verdict']
    list_per_page = 20
    ordering = ['participant__username', 'court__name', 'relief_type', 'verdict']
    fieldsets = [
        ('Relief Information', {
            'fields': ['participant', 'court', 'relief_type', 'verdict', 'value']}),
    ]


admin.site.register(Relief, ReliefAdmin)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_id', 'invoice_type', 'invoice_status', 'invoice_amount', 'invoice_date',
                    'invoice_due_date', 'case_proceeding', 'created_by', 'created_on', 'transaction', 'relieved_by']
    list_filter = ['invoice_type', 'invoice_status', 'case_proceeding', 'created_by', 'transaction', 'relieved_by']
    search_fields = ['invoice_id', 'invoice_type', 'invoice_status', 'case_proceeding__document_name',
                     'created_by__username', 'relieved_by__participant__username']
    list_per_page = 20
    ordering = ['invoice_id', 'invoice_type', 'invoice_status', 'case_proceeding__document_name',
                'created_by__username', 'relieved_by__participant__username']
    fieldsets = [
        ('Invoice Information', {
            'fields': ['invoice_id', 'invoice_type', 'invoice_status', 'invoice_amount',
                       'invoice_due_date', 'case_proceeding', 'created_by', 'transaction', 'relieved_by']}),
    ]


admin.site.register(Invoice, InvoiceAdmin)


class PaymentQueueAdmin(admin.ModelAdmin):
    # values: checkout_request_id, phone_number, account_reference, amount, status, created_on, invoice, transaction
    list_display = ['checkout_request_id', 'phone_number', 'account_reference', 'transaction_description', 'amount', 'status', 'created_on',
                    'invoice', 'transaction']
    list_filter = ['status', 'invoice', 'transaction', 'transaction_description']
    search_fields = ['checkout_request_id', 'phone_number', 'account_reference', 'amount', 'status', 'created_on',
                     'invoice', 'transaction']
    list_per_page = 20
    ordering = ['checkout_request_id', 'phone_number', 'account_reference', 'amount', 'status', 'created_on', 'invoice',
                'transaction']

    fieldsets = [
        ('Payment Queue Information', {
            'fields': ['checkout_request_id', 'phone_number', 'account_reference', 'transaction_description', 'amount', 'status',
                       'invoice', 'transaction']
        }),
    ]


admin.site.register(PaymentQueue, PaymentQueueAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_no', 'phone_number', 'checkout_request_id', 'mpesa_reference', 'description', 'participant', 'amount',
                    'payment_status', 'receipt_id', 'created_on', 'paid_for', 'invoice']
    list_filter = ['payment_status', 'paid_for', 'invoice']
    search_fields = ['transaction_no', 'phone_number', 'checkout_request_id', 'mpesa_reference', 'description',
                     'amount',
                     'payment_status', 'receipt_id', 'created_on', 'paid_for', 'invoice']
    list_per_page = 20
    ordering = ['transaction_no', 'phone_number', 'checkout_request_id', 'mpesa_reference', 'description', 'amount',
                'payment_status',
                'receipt_id', 'created_on', 'paid_for', 'invoice']
    fieldsets = [
        ('Transaction Information', {
            'fields': ['transaction_no', 'phone_number', 'checkout_request_id', 'mpesa_reference', 'description',  'participant',
                       'amount', 'payment_status', 'receipt_id', 'paid_for', 'invoice']}),
    ]


admin.site.register(Transaction, TransactionAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'subject']
    search_fields = ['first_name', 'last_name', 'email', 'phone', 'subject']
    list_per_page = 20
    ordering = ['first_name', 'last_name', 'email', 'phone', 'subject']


admin.site.register(Contact, ContactAdmin)

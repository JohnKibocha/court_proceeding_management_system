from django.urls import path

from . import views

urlpatterns = [

    # system-wide paths
    path('', views.IndexView.as_view(), name='index'),
    path('contact', views.ContactView.as_view(), name='contact'),
    path('success', views.SuccessView.as_view(), name='success'),
    path('sidebar', views.SidebarView.as_view(), name='sidebar'),

    # authentication paths
    path('register', views.RegisterView.as_view(), name='register'),
    path('login', views.LoginView.as_view(), name='login'),
    path('logout', views.UserLogoutView.as_view(), name='logout'),
    path('pending-approval', views.PendingApprovalView.as_view(), name='pending-approval'),
    path('dashboard', views.DashboardView.as_view(), name='dashboard'),

    # admin paths
    # admin manage clerks
    path('admin-manage-clerk', views.AdminManageClerksView.as_view(), name='admin-manage-clerk'),
    path('admin-create-clerk', views.AdminCreateClerkView.as_view(), name='admin-create-clerk'),
    path('admin-edit-clerk/<int:user_id>', views.AdminEditClerkView.as_view(), name='admin-edit-clerk'),
    path('admin-delete-clerk/<int:user_id>', views.AdminDeleteClerkView.as_view(), name='admin-delete-clerk'),
    # admin manage courts
    path('admin-manage-court', views.AdminManageCourtView.as_view(), name='admin-manage-court'),
    path('admin-create-court', views.AdminCreateCourtView.as_view(), name='admin-create-court'),
    path('admin-edit-court/<int:court_id>', views.AdminEditCourtView.as_view(), name='admin-edit-court'),
    path('admin-delete-court/<int:court_id>', views.AdminDeleteCourtView.as_view(), name='admin-delete-court'),
    # admin manage judges
    path('admin-manage-judge', views.AdminManageJudgeView.as_view(), name='admin-manage-judge'),
    path('admin-create-judge', views.AdminCreateJudgeView.as_view(), name='admin-create-judge'),
    path('admin-edit-judge/<int:user_id>', views.AdminEditJudgeView.as_view(), name='admin-edit-judge'),
    path('admin-delete-judge/<int:user_id>', views.AdminDeleteJudgeView.as_view(), name='admin-delete-judge'),
    path('manage-profile/<int:user_id>', views.ManageProfileView.as_view(), name='manage-profile'),

    # clerk paths
    # clerk manage participants
    path('clerk-manage-participant', views.ClerkManageParticipantView.as_view(), name='clerk-manage-participant'),
    path('clerk-create-participant', views.ClerkCreateParticipantView.as_view(), name='clerk-create-participant'),
    path('clerk-approve-participant/<int:user_id>', views.ClerkApproveParticipantView.as_view(), name='clerk-approve-participant'),
    path('clerk-delete-participant/<int:user_id>', views.ClerkDeleteParticipantView.as_view(), name='clerk-delete-participant'),
    # clerk manage cases
    path('clerk-manage-case', views.ClerkManageCaseView.as_view(), name='clerk-manage-case'),
    path('clerk-create-case', views.ClerkCreateCaseView.as_view(), name='clerk-create-case'),
    path('clerk-edit-case/<int:case_id>', views.ClerkEditCaseView.as_view(), name='clerk-edit-case'),
    path('clerk-delete-case/<int:case_id>', views.ClerkDeleteCaseView.as_view(), name='clerk-delete-case'),

    # participants paths
    # participant manage cases
    path('participant-manage-case', views.ParticipantManageCaseView.as_view(), name='participant-manage-case'),

    # manage proceeding paths
    path('manage-case-proceeding/<int:case_id>', views.ManageCaseProceedingView.as_view(), name='manage-case-proceeding'),
    path('create-case-proceeding/<int:case_id>', views.CreateCaseProceedingView.as_view(), name='create-case-proceeding'),
    path('view-case-proceeding/<int:case_proceeding_id>', views.ViewCaseProceedingView.as_view(), name='view-case-proceeding'),
    path('edit-case-proceeding/<int:case_proceeding_id>', views.EditCaseProceedingView.as_view(), name='edit-case-proceeding'),
    path('delete-case-proceeding/<int:case_proceeding_id>', views.DeleteCaseProceedingView.as_view(), name='delete-case-proceeding'),
    path('download-case-proceeding-document/<int:case_proceeding_id>', views.DownloadCaseProceedingDocumentView.as_view(), name='download-case-proceeding-document'),


    # manage invoices
    path('manage-invoice', views.ManageInvoiceView.as_view(), name='manage-invoice'),
    path('select-participant-for-invoice/<int:case_proceeding_id>', views.SelectParticipantForInvoiceView.as_view(), name='select-participant-for-invoice'),
    path('create-invoice/<int:case_proceeding_id>/<int:participant_id>', views.CreateInvoiceView.as_view(), name='create-invoice'),
    path('edit-invoice/<int:invoice_id>', views.EditInvoiceView.as_view(), name='edit-invoice'),
    path('delete-invoice/<int:invoice_id>', views.DeleteInvoiceView.as_view(), name='delete-invoice'),
    path('view-invoice/<int:invoice_id>', views.ViewInvoiceView.as_view(), name='view-invoice'),
    path('download-invoice/<int:invoice_id>', views.DownloadInvoiceView.as_view(), name='download-invoice'),


    # manage payments
    path('daraja/stk_push', views.stk_push_callback, name='stk_push_callback'),
    path('manage-payment', views.ManagePaymentView.as_view(), name='manage-payment'),
    path('create-payment/<int:invoice_id>', views.CreatePaymentView.as_view(), name='create-payment'),
    path('view-payment-receipt/<int:payment_id>', views.ViewPaymentReceiptView.as_view(), name='view-payment-receipt'),
    path('download-payment-receipt/<int:payment_id>', views.DownloadPaymentReceiptView.as_view(), name='download-payment-receipt'),


    # header and footer paths
    path('header', views.HeaderView.as_view(), name='header'),
    path('footer', views.FooterView.as_view(), name='footer'),
]

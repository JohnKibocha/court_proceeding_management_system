import uuid

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import re


# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.subject})'


class User(AbstractUser, PermissionsMixin):
    ROLES = (
        ('admin', 'Admin'),
        ('clerk', 'Clerk'),
        ('judge', 'Judge'),
        ('participant', 'Participant'),
        ('lawyer', 'Lawyer'),
    )

    COUNTY_CHOICES = (
        ('Baringo', 'Baringo'),
        ('Bomet', 'Bomet'),
        ('Bungoma', 'Bungoma'),
        ('Busia', 'Busia'),
        ('Elgeyo Marakwet', 'Elgeyo Marakwet'),
        ('Embu', 'Embu'),
        ('Garissa', 'Garissa'),
        ('Homa Bay', 'Homa Bay'),
        ('Isiolo', 'Isiolo'),
        ('Kajiado', 'Kajiado'),
        ('Kakamega', 'Kakamega'),
        ('Kericho', 'Kericho'),
        ('Kiambu', 'Kiambu'),
        ('Kilifi', 'Kilifi'),
        ('Kirinyaga', 'Kirinyaga'),
        ('Kisii', 'Kisii'),
        ('Kisumu', 'Kisumu'),
        ('Kitui', 'Kitui'),
        ('Kwale', 'Kwale'),
        ('Laikipia', 'Laikipia'),
        ('Lamu', 'Lamu'),
        ('Machakos', 'Machakos'),
        ('Makueni', 'Makueni'),
        ('Mandera', 'Mandera'),
        ('Marsabit', 'Marsabit'),
        ('Meru', 'Meru'),
        ('Migori', 'Migori'),
        ('Mombasa', 'Mombasa'),
        ('Murang\'a', 'Murang\'a'),
        ('Nairobi', 'Nairobi'),
        ('Nakuru', 'Nakuru'),
        ('Nandi', 'Nandi'),
        ('Narok', 'Narok'),
        ('Nyamira', 'Nyamira'),
        ('Nyandarua', 'Nyandarua'),
        ('Nyeri', 'Nyeri'),
        ('Samburu', 'Samburu'),
        ('Siaya', 'Siaya'),
        ('Taita Taveta', 'Taita Taveta'),
        ('Tana River', 'Tana River'),
        ('Tharaka Nithi', 'Tharaka Nithi'),
    )

    TRIBE_CHOICES = (
        # add all tribes in Kenya
        ('Kikuyu', 'Kikuyu'),
        ('Luhya', 'Luhya'),
        ('Luo', 'Luo'),
        ('Kalenjin', 'Kalenjin'),
        ('Kamba', 'Kamba'),
        ('Kisii', 'Kisii'),
        ('Mijikenda', 'Mijikenda'),
        ('Meru', 'Meru'),
        ('Turkana', 'Turkana'),
        ('Maasai', 'Maasai'),
        ('Embu', 'Embu'),
        ('Taita', 'Taita'),
        ('Giriama', 'Giriama'),
        ('Rendille', 'Rendille'),
        ('Borana', 'Borana'),
        ('Samburu', 'Samburu'),
        ('Pokomo', 'Pokomo'),
        ('Orma', 'Orma'),
        ('Elmolo', 'Elmolo'),
        ('Digo', 'Digo'),
        ('Swahili', 'Swahili'),
        ('Taveta', 'Taveta'),
        ('Kuria', 'Kuria'),
        ('Mbeere', 'Mbeere'),
        ('Tharaka', 'Tharaka'),
        ('Gusii', 'Gusii'),
        ('Ilchamus', 'Ilchamus'),
        ('Kalenjin', 'Kalenjin'),
        ('Kamba', 'Kamba'),
        ('Kikuyu', 'Kikuyu'),
        ('Kisii', 'Kisii'),
        ('Kuria', 'Kuria'),
        ('Luhya', 'Luhya'),
        ('Luo', 'Luo'),
        ('Maasai', 'Maasai'),
        ('Meru', 'Meru'),
        ('Mijikenda', 'Mijikenda'),
        ('Pokomo', 'Pokomo'),
        ('Rendille', 'Rendille'),
        ('Samburu', 'Samburu'),
        ('Somali', 'Somali'),
        ('Swahili', 'Swahili'),
        ('Taita', 'Taita'),
        ('Taveta', 'Taveta'),
        ('Tharaka', 'Tharaka'),
        ('Turkana', 'Turkana'),
        ('Gabra', 'Gabra'),
        ('Giriama', 'Giriama'),
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('prefer not to say', 'Prefer not to say'),
    )

    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True, default='profile_images'
                                                                                                  '/default.png')
    user_id = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30, choices=ROLES, default='observer')
    national_id = models.IntegerField(unique=True)
    county_of_residence = models.CharField(max_length=30, choices=COUNTY_CHOICES, default='Nairobi')
    phone_number = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=30, choices=GENDER_CHOICES, default='prefer not to say')
    tribe = models.CharField(max_length=30, choices=TRIBE_CHOICES, default='Kikuyu')
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    password = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    # relationships
    courts = models.ManyToManyField('Court', related_name='users', blank=True)

    @property
    def is_authenticated(self):
        return bool(self.username and self.password)

    # create all user ids with format 'USER-0001' etc
    def save(self, *args, **kwargs):
        if not self.user_id:
            last_user = User.objects.all().order_by('user_id').last()
            if not last_user:
                self.user_id = 'USR-0001'
            else:
                self.user_id = 'USR-%04d' % (last_user.id + 1)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Court(models.Model):
    COURT_TYPES = (
        ('high court', 'High Court'),
        ('magistrate court', 'Magistrate Court'),
        ('environment court', 'Environment and Land Court'),
        ('labour court', 'Employment and Labour Court'),
        ('anti-corruption court', 'Anti-Corruption Court'),
        ('children court', 'Children\'s Court'),
        ('maritime court', 'Maritime Court'),
        ('military court', 'Military Court'),
        ('tax court', 'Tax Court'),
        ('appeal court', 'Court of Appeal'),
        ('supreme court', 'Supreme Court'),
    )

    name = models.CharField(max_length=255)
    court_id = models.CharField(max_length=30, unique=True)
    court_logo = models.ImageField(upload_to='court_logos/', null=True, blank=True,
                                   default='../static/images/default_court.png')
    court_email = models.EmailField()
    court_phone = models.CharField(max_length=15, blank=True)
    court_address = models.CharField(max_length=255)
    location = models.CharField(max_length=255, choices=User.COUNTY_CHOICES)
    court_type = models.CharField(max_length=255, choices=COURT_TYPES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    # create all court ids with format 'court-0001' etc
    def save(self, *args, **kwargs):
        if not self.court_id:
            last_court = Court.objects.all().order_by('court_id').last()
            if not last_court:
                self.court_id = 'CRT-0001'
            else:
                self.court_id = 'CRT-%04d' % (last_court.id + 1)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} ({self.location})'


class Case(models.Model):
    CASE_TYPES = (
        ('civil', 'Civil'),
        ('criminal', 'Criminal'),
        ('family', 'Family'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
        ('labour', 'Labour'),
        ('constitutional', 'Constitutional'),
        ('environmental', 'Environmental'),
        ('appeal', 'Appeal'),
        ('miscellaneous', 'Miscellaneous'),
    )

    CASE_STATUS = (
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('concluded', 'Concluded'),
    )

    DECISION_CHOICES = (
        ('dismissed', 'Dismissed'),
        ('upheld', 'Upheld'),
        ('overturned', 'Overturned'),
        ('compensated', 'Compensated'),
        ('acquitted', 'Acquitted'),
        ('convicted', 'Convicted'),
        ('sentenced', 'Sentenced'),
        ('fined', 'Fined'),
        ('imprisoned', 'Imprisoned'),
        ('community service', 'Community Service'),
        ('probation', 'Probation'),
        ('parole', 'Parole'),
        ('suspended sentence', 'Suspended Sentence'),
        ('death penalty', 'Death Penalty'),
        ('life imprisonment', 'Life Imprisonment'),
        ('acquitted', 'Acquitted'),
        ('discharged', 'Discharged'),
        ('reprimanded', 'Reprimanded'),
        ('warned', 'Warned'),
        ('rehabilitated', 'Rehabilitated'),
        ('restitution', 'Restitution'),
        ('compensation', 'Compensation'),
        ('damages', 'Damages'),
        ('injunction', 'Injunction'),
        ('restraining order', 'Restraining Order'),
        ('restitution', 'Restitution'),
        ('reparations', 'Reparations'),
    )

    case_id = models.CharField(max_length=30, unique=True)
    case_type = models.CharField(max_length=30, choices=CASE_TYPES, default='miscellaneous')
    case_status = models.CharField(max_length=30, choices=CASE_STATUS, default='pending')
    case_name = models.CharField(max_length=255)
    defendants = models.ManyToManyField(User, related_name='defendants', blank=True)
    plaintiffs = models.ManyToManyField(User, related_name='plaintiffs', blank=True)
    judges = models.ManyToManyField(User, related_name='judges', blank=True)
    clerks = models.ManyToManyField(User, related_name='clerks', blank=True)
    lawyers = models.ManyToManyField(User, related_name='lawyers', blank=True)
    amicus = models.ManyToManyField(User, related_name='amicus', blank=True)
    observers = models.ManyToManyField(User, related_name='observers', blank=True)
    case_description = models.TextField(blank=True, null=True)
    relief_sought = models.TextField(blank=True, null=True)
    decision = models.TextField(blank=True, null=True, choices=DECISION_CHOICES)
    date_filed = models.DateField()
    date_hearing = models.DateField()
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    # create all case ids with format 'case-0001' etc
    def save(self, *args, **kwargs):
        if not self.case_id:
            last_case = Case.objects.all().order_by('case_id').last()
            if not last_case:
                self.case_id = 'CSE-0001'
            else:
                self.case_id = 'CSE-%04d' % (last_case.id + 1)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.case_name} ({self.case_type} case)'


class Relief(models.Model):
    RELIEF_TYPES = (
        ('monetary', 'Monetary'),
        ('custodial', 'Custodial'),
    )

    VERDICT_CHOICES = (
        ('dismissed', 'Dismissed'),
        ('upheld', 'Upheld'),
        ('overturned', 'Overturned'),
        ('compensated', 'Compensated'),
        ('acquitted', 'Acquitted'),
        ('convicted', 'Convicted'),
        ('sentenced', 'Sentenced'),
        ('fined', 'Fined'),
        ('imprisoned', 'Imprisoned'),
        ('community service', 'Community Service'),
        ('probation', 'Probation'),
        ('parole', 'Parole'),
        ('suspended sentence', 'Suspended Sentence'),
        ('death penalty', 'Death Penalty'),
        ('life imprisonment', 'Life Imprisonment'),
        ('acquitted', 'Acquitted'),
        ('discharged', 'Discharged'),
        ('reprimanded', 'Reprimanded'),
        ('warned', 'Warned'),
        ('rehabilitated', 'Rehabilitated'),
        ('restitution', 'Restitution'),
        ('compensation', 'Compensation'),
        ('damages', 'Damages'),
        ('injunction', 'Injunction'),
        ('restraining order', 'Restraining Order'),
        ('restitution', 'Restitution'),
        ('reparations', 'Reparations'),
    )
    participant = models.ForeignKey(User, on_delete=models.CASCADE)
    court = models.ForeignKey(Court, on_delete=models.CASCADE)
    relief_type = models.CharField(max_length=10, choices=RELIEF_TYPES)
    verdict = models.CharField(max_length=255, choices=VERDICT_CHOICES)
    case_proceeding = models.ForeignKey('CaseProceeding', on_delete=models.CASCADE)
    value = models.IntegerField()

    def __str__(self):
        return f'{self.participant} - Relief: {self.relief_type} - Verdict: {self.verdict} - of  {self.value}'


class CaseProceeding(models.Model):
    DOCUMENT_TYPES = (
        ('evidence', 'Evidence'),
        ('order', 'Order'),
        ('report', 'Report'),
        ('motion', 'Motion'),
        ('judgement', 'Judgement'),
        ('opinion', 'Opinion'),
        ('agreement', 'Agreement'),
        ('statement', 'Statement'),
        ('notice', 'Notice'),
        ('affidavit', 'Affidavit'),
        ('brief', 'Brief'),
        ('complaint', 'Complaint'),
        ('memorandum', 'Memorandum'),
        ('declaration', 'Declaration'),
        ('deposition', 'Deposition'),
        ('pleading', 'Pleading'),
        ('petition', 'Petition'),
        ('reply', 'Reply'),
        ('warrant', 'Warrant'),
        ('will', 'Will'),
        ('subpoena', 'Subpoena'),
        ('transcript', 'Transcript'),
        ('verdict', 'Verdict'),
        ('appeal', 'Appeal'),
        ('sentence', 'Sentence'),
        ('ruling', 'Ruling'),
        ('decree', 'Decree'),
        ('directive', 'Directive'),
        ('mandate', 'Mandate'),
        ('injunction', 'Injunction'),
        ('citation', 'Citation'),
        ('summons', 'Summons'),
        ('writ', 'Writ')
    )

    CONFIDENTIALITY_LEVELS = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    )

    document_id = models.CharField(max_length=30, unique=True)
    document_name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPES)
    filed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    filed_as = models.CharField(max_length=255, choices=User.ROLES)
    filed_on = models.DateTimeField(auto_now_add=True)
    confidentiality = models.CharField(max_length=30, choices=CONFIDENTIALITY_LEVELS)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    editors = models.ManyToManyField(User, related_name='editors', blank=True)
    content = RichTextUploadingField(null=True, blank=True, default='')
    reliefs = models.ManyToManyField(Relief, blank=True)

    def save(self, *args, **kwargs):
        if not self.document_id:
            last_document = CaseProceeding.objects.all().order_by('document_id').last()
            if not last_document:
                self.document_id = 'DOC-0001'
            else:
                self.document_id = 'DOC-%04d' % (last_document.id + 1)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.document_name} ({self.document_type})'


class Invoice(models.Model):
    # these are invoices for court proceedings, particularly for the CaseProceeding model according to the selected relief model values by the judge
    INVOICE_TYPES = (
        ('court fees', 'Court Fees'),
        ('legal fees', 'Legal Fees'),
        ('filing fees', 'Filing Fees'),
        ('service fees', 'Service Fees'),
        ('miscellaneous', 'Miscellaneous'),
    )

    INVOICE_STATUS = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )

    invoice_id = models.CharField(max_length=30, unique=True)
    invoice_type = models.CharField(max_length=30, choices=INVOICE_TYPES, default='miscellaneous')
    invoice_status = models.CharField(max_length=30, choices=INVOICE_STATUS, default='pending')
    invoice_amount = models.IntegerField()
    participant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participant', default='')
    invoice_date = models.DateField(auto_now_add=True)
    invoice_due_date = models.DateField()
    case_proceeding = models.ForeignKey(CaseProceeding, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    relieved_by = models.ForeignKey(Relief, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.invoice_id:
            last_invoice = Invoice.objects.all().order_by('invoice_id').last()
            if not last_invoice:
                self.invoice_id = 'INV-0001'
            else:
                self.invoice_id = 'INV-%04d' % (last_invoice.id + 1)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f' {self.invoice_id} (KES {self.invoice_amount})'


# function to generate unique transaction numbers for each transaction

def next_letter_sequence(seq):
    if seq == 'ZZZZ':
        return 'AAAA'
    last_char = seq[-1]
    if last_char != 'Z':
        return seq[:-1] + chr(ord(last_char) + 1)
    else:
        return next_letter_sequence(seq[:-1]) + 'A'


def next_digit_sequence(seq):
    if seq == '999999':
        return '654321'
    return str(int(seq) + 1).zfill(6)


def next_two_letter_sequence(seq):
    if seq == 'ZZ':
        return 'DG'
    last_char = seq[-1]
    if last_char != 'Z':
        return seq[:-1] + chr(ord(last_char) + 1)
    else:
        return seq[0] + 'A'


# Transaction model for payment processing
class Transaction(models.Model):
    STATUS_CHOICES = (
        (0, 'Pending'),
        (1, 'Complete'),
        (2, 'Failed'),
        (3, 'Cancelled'),
        (4, 'Refunded'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('complete', 'Complete'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    )

    transaction_no = models.CharField(max_length=50, unique=True)
    phone_number = PhoneNumberField(null=False, blank=False)
    checkout_request_id = models.CharField(max_length=200)
    reference = models.CharField(max_length=40, blank=True)
    description = models.TextField(null=True, blank=True)
    amount = models.CharField(max_length=10)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=1)
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS_CHOICES, default='pending')
    receipt_no = models.CharField(max_length=200, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=200, blank=True, null=True)
    paid_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoice_recepient', default='')
    paid_by = models.CharField(max_length=200, blank=True, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice', default='')

    def __str__(self):
        return f'Transaction {self.transaction_no} - {self.amount}'

    def save(self, *args, **kwargs):
        if not self.transaction_no:
            last_transaction = Transaction.objects.all().order_by('-id').first()
            if last_transaction is None:
                self.transaction_no = 'ABCD654321DG'
            else:
                parts = re.match(r'([A-Z]{4})(\d{6})([A-Z]{2})', last_transaction.transaction_no)
                letter_seq = next_letter_sequence(parts.group(1))
                digit_seq = next_digit_sequence(parts.group(2))
                two_letter_seq = next_two_letter_sequence(parts.group(3))
                if two_letter_seq == 'DG':
                    if digit_seq == '654321':
                        letter_seq = next_letter_sequence(letter_seq)
                    else:
                        digit_seq = next_digit_sequence(digit_seq)
                self.transaction_no = letter_seq + digit_seq + two_letter_seq

        if self.status == 1:
            self.invoice.invoice_status = 'paid'
            self.invoice.save()
            self.payment_status = 'complete'
        elif self.status == 2:
            self.invoice.invoice_status = 'pending'
            self.invoice.save()
            self.payment_status = 'failed'
        elif self.status == 3:
            self.invoice.invoice_status = 'pending'
            self.invoice.save()
            self.payment_status = 'cancelled'
        elif self.status == 4:
            self.invoice.invoice_status = 'pending'
            self.invoice.save()
            self.payment_status = 'refunded'

        super().save(*args, **kwargs)

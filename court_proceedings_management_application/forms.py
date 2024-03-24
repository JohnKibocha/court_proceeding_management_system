# forms.py
from django import forms

from .models import CaseProceeding


class CaseProceedingForm(forms.ModelForm):
    class Meta:
        model = CaseProceeding
        fields = ['content',]
        labels = {
            'content': 'Document Content'
        }


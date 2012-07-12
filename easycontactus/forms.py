from django import forms
from django.template.loader import render_to_string
from django.conf import settings
from ckeditor.widgets import CKEditorWidget
import datetime
import calendar
from django.forms.widgets import RadioSelect, CheckboxSelectMultiple
from django.core.exceptions import ValidationError
class  ContactUsForm(forms.Form):
    ### form settings and configuration
    FIND_US_CHOICES = (
                       ('Internet Search', 'Internet Search'),
                       ('Word of Mouth', 'Word of Mouth'),
                       ('Internet Search', 'Internet Search'),
                       )
    CAPTHCA_PHRASE = 'multiple' #captcha phrase to match
    # django native
    #error_css_class = 'clsError' # defaults to .error class
    required_css_class = 'required'

    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=12)
    email = forms.EmailField(help_text='Enter a valid email')
    found_us = forms.CharField(label='How you found us')
    message = forms.CharField(widget=forms.Textarea())
    captcha = forms.RegexField(max_length=20, regex=CAPTHCA_PHRASE, error_messages={'invalid': 'Type it exactly as it appears.'})


from django import forms
from django.template.loader import render_to_string
from django.conf import settings
from ckeditor.widgets import CKEditorWidget
import datetime
import calendar
from django.core.exceptions import ValidationError


EMPTY_VALUES = (None, '')

class HoneypotWidget(forms.TextInput):
    is_hidden = True
    def __init__(self, attrs=None, html_comment=False, *args, **kwargs):
        self.html_comment = html_comment
        super(HoneypotWidget, self).__init__(attrs, *args, **kwargs)
        if not self.attrs.has_key('class'):
            self.attrs['style'] = 'display:none'
    def render(self, *args, **kwargs):
        value = super(HoneypotWidget, self).render(*args, **kwargs)
        if self.html_comment:
            value = '<!-- %s -->' % value
        return value

class HoneypotField(forms.Field):
    """
    In the following example, only the email field will be visible (the
    HoneypotFields are named as such to increase the chance that a bot
    will try to fill them in):
    
    class EmailForm(Form):
       name = HoneypotField()
       website = HoneypotField(initial='leave me')
    email = EmailField()
    """
    widget = HoneypotWidget
    def clean(self, value):
        if self.initial in EMPTY_VALUES and value in EMPTY_VALUES or value == self.initial:
            return value
        raise ValidationError('Anti-spam field changed in value.')


class  ContactUsForm(forms.Form):
    ### form settings and configuration
    CAPTHCA_PHRASE = 'multiple' #captcha phrase to match

    # django native
    required_css_class = 'required' # when specified ads a class=required to required 'rows' when rendering

    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=12)
    email = forms.EmailField()
    found_us = forms.CharField(label='How did you find us')
    message = forms.CharField(widget=forms.Textarea())
    captcha = forms.RegexField(max_length=20,
                               help_text='Enter a word or phrase "%s"' % CAPTHCA_PHRASE,
                               regex='^%s$' % CAPTHCA_PHRASE,
                               error_messages={'invalid': 'Incorrect phrase, please try again.'})
    honeypot = HoneypotField(initial='hello there')


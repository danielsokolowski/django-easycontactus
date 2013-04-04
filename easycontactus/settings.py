"""
Default application settings imported through modules __init__.

Settings defined on project level settings.py file take precedence over these defaults.
"""
from .forms import *
from django import forms
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

### Defaults and globals
# Contact form class to be used - develoeprs can specify their own custom form
CONTACT_FORM_CLASS = getattr(settings, 'EASYCONTACTUS_CONTACT_FORM_CLASS', EasyContactUsForm)

### Sanity checks
if not issubclass(CONTACT_FORM_CLASS, forms.Form):
	raise ImproperlyConfigured("EASYCONTACTUS_CONTACT_FORM_CLASS must be an instance of `<class 'django.forms.forms.Form'>` but instead is: {0!r} ({1})".format(forms.Form, type(forms.Form)))

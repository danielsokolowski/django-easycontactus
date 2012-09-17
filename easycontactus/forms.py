from django import forms
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


class  EasyContactUsForm(forms.Form):
    ### form settings and configuration
    CAPTHCA_PHRASE = 'multiple' #captcha phrase to match
    def __init__(self, *args, **kwargs):
        super(EasyContactUsForm, self).__init__(*args, **kwargs)
        # we redefine captcha at run time so that CAPTHCA_PHRASE is loaded
        # from child properly if this form is extended, other wise depending 
        # when super call to this class is called we might end up with the CAPTHCA_PHRASE
        # from this this class and not our overiden child class
        self.fields['captcha'] = forms.RegexField(max_length=20,
                               help_text='Enter the word or phrase "%s"' % self.CAPTHCA_PHRASE,
                               regex='^%s$' % self.CAPTHCA_PHRASE,
                               error_messages={'invalid': 'Incorrect phrase, please try again.'})

    # django native
    required_css_class = 'required' # when specified ads a class=required to required 'rows' when rendering
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=12)
    email = forms.EmailField()
    found_us = forms.CharField(label='How did you find us')
    message = forms.CharField(widget=forms.Textarea())
    captcha = forms.RegexField(max_length=20, regex='') # properly defined at run time in __init__
    honeypot = HoneypotField(initial='hello there')


django-easycontactus
====================

Plain, straightforward extendable skeleton contact us form with dynamic form content aggregation and spam prevention. 

Overview
--------

Consider this a starting code base that you can tailor to your project needs rather than a stand alone Django app. 
It is recommend you place it directly in your project and adjust accordingly. Emails are sent to addresses listed in
your 'MANAGERS' project 'setting.py' and the body of the message automatically includes any new fields added to 
the form trough introspection. The form does include basic spam prevention with a 'honey pot' and 'captcha' fields.

A form defined as follows:
	
	# easycontacts/forms.py
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

Will result in the following email message generated:

	 **Name**
	Daniel Sokolowski
	
	**Phone**
	(613) 817-6833
	
	**Email**
	testing@danols.com
	
	**How did you find us:**
	Testing
	
	**Message:**
	test
		 
Installation
------------

Copy 'easycontactus' into your django project root and add it to your 'INSTALLED_APPS' settings and tie it into 
your projects 'urls.py' file by adding 'url(r'^contact-us/', include('easycontactus.urls')),' line to it.  

Stand alone app
---------------

If you insist on installing this as a stand alone know then you can specify a custom form class with 
the `EASYCONTACTUS_CONTACT_FORM_CLASS` parameter placed in your projects `settings.py` file; to keep things obvious 
you can do so as follows:

	# settings.py
	
	...
	
	### django-easycontactus settings
	from easycontactus.forms import *
	from django import forms
	class  CustomEasyContactUsForm(EasyContactUsForm):
		### form settings and configuration
		CAPTHCA_PHRASE = 'igolfmuch'
	
		### native methods
		def __init__(self, *args, **kwargs):
			self.CAPTHCA_PHRASE = 'igolf'
			super(CustomEasyContactUsForm, self).__init__(*args, **kwargs)
			# re-order placement of added attachment field 
			self.fields.keyOrder.insert(self.fields.keyOrder.index('captcha'),
										self.fields.keyOrder.pop(self.fields.keyOrder.index('attachment'))
										)
	
		### field defintitions
		attachment = forms.FileField(required=False)
	EASYCONTACTUS_CONTACT_FORM_CLASS = CustomEasyContactUsForm 

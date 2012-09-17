django-easycontactus
====================

Plain, no bells or whistles extendable skeleton contact us form with dynamic form content aggregation. 

Consider this a starting code base that you can tailor to your project needs rather than a stand alone Django app. 
It is recommend you place it directly in your project and adjust accordingly. Emails are sent to addresses listed in
your 'MANAGERS' project 'setting.py' and the body of the message automatically includes any new fields added to 
the form trough introspection. 

When installed as a stand alone app you can specify a custom form class with the `EASYCONTACTUS_CONTACT_FORM_CLASS`
parameter placed in your projects `settings.py` file; to keep things straightforward you can do so as follows:

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

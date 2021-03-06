# Create your views here.
#from .forms import *
from .settings import *

from django.conf import settings
from django.views.generic import FormView
from django.core.mail import EmailMessage
from django.contrib import messages
class EasyContactUsIndexView(FormView):
	"""  
	Index view to display a contact us form and process POST requests for it. 
	
	If POST request results in a valid FORM the contents of the form are emailed
	to mangers specified by `settings.MANAGERS`
	
	**Templates**
	
		:template:`contactus/index.html`
		
	**Context**
		
	Adds following variables to the template context scope:
		
		``form``, ``contactus`` - a data bound or unbound (empty) form 
	"""
	### view's settings
	# TemplateResponseMixin
	template_name = 'easycontactus/index.html'
	# FormView(FormMixing, ProcessFormView) settings
	form_class = CONTACT_FORM_CLASS
	success_url = './'

	### view's methods overrides 
	def get_context_data(self, **kwargs):
		""" Adds extra content to our template """
		context = super(EasyContactUsIndexView, self).get_context_data(**kwargs)
		form_class = self.get_form_class()
		form = form_class(data=self.request.POST, files=self.request.FILES) #unbound
		context['contact_us_form'] = form
		return context

	def form_valid(self, form):
		""" extract form data and email it """
		#form_class = self.get_form_class()
		#form = self.get_form(form_class)
		form.full_clean() # call full_clean to populate .cleaned_data
		subject = '%s %s by %s ' % (settings.EMAIL_SUBJECT_PREFIX, form.__class__.__name__, form.cleaned_data['name'])
		to = [x[1] for x in  settings.MANAGERS]
		from_email = form.cleaned_data['email']
		headers = {'Reply-To': from_email}
		message = '' # will hold message

		for key, field in form.fields.iteritems():
			field_label = (field.label or key).capitalize()
			value = form.cleaned_data[key]
			# skip some built in fields we don't need to use for the message
			if 'honeypot' == key or 'captcha' == key:
				continue
			message = message + '**%s**\n%s\n\n' % (field_label, value)
			
		email = EmailMessage(subject=subject, body=message, from_email=from_email,
			to=to, bcc=[], headers=headers)

		# do attachments
		for key, field in form.fields.iteritems():
			file = self.request.FILES.get(key, None)
			if file:
				email.attach('%s-%s' % (field.label or key, file.name), file.read(), file.content_type)

		email.send()

		messages.success(self.request, 'Your form has been submitted.')
		return super(EasyContactUsIndexView, self).form_valid(form)


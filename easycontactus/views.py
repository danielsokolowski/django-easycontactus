# Create your views here.
from .forms import *
from django.conf import settings
from django.views.generic import FormView
from django.core.mail import EmailMessage
from django.contrib import messages
class ContactUsIndexView(FormView):
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
    template_name = 'contactus/index.html'
    # FormView(FormMixing, ProcessFormView) settings
    form_class = ContactUsForm
    success_url = './'

    ### view's methods overrides 
    def get_context_data(self, **kwargs):
        """ Adds extra content to our template """
        context = super(ContactUsIndexView, self).get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = form_class() #unbound
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
            value = form.cleaned_data[key]
            message = message + '%s: %s\n' % (field.label or key, value)

        email = EmailMessage(subject=subject, body=message, from_email=from_email,
            to=to, bcc=[], headers=headers)

        # do attachments
        for key, field in form.fields.iteritems():
            file = self.request.FILES.get(key, None)
            if file:
                email.attach('%s-%s' % (field.label or key, file.name), file.read(), file.content_type)

        email.send()

        messages.success(self.request, 'Your form has been submitted.')
        return super(ContactUsIndexView, self).form_valid(form)


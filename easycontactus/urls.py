from .views import *
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
	# Only one view, this urls.py is reference in django-project/urls.py see there
	# the r'...' is a regular expression patter that matches an emtpy string --- project
	# urls.py must matches some other part of the url consumes it and passes the reminder
	# to this list. Read this # https://docs.djangoproject.com/en/dev/topics/http/urls/
	url(r'^$', EasyContactUsIndexView.as_view(), name='EasyContactUsIndexView'),
)

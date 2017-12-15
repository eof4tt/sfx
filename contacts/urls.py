from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required, login_required
from contacts.views import ContactDetailView, ContactCreate, ContactUpdate
from . import views

urlpatterns = patterns('',
  url(r'^index/$', views.contacts_list, name = "contacts_index"),
  url(r'^(?P<pk>\d+)/$', permission_required("sufix.add_contacts")(ContactDetailView.as_view()), name="contacts_detail"),
  url(r'^add/(?:(?P<prtnr>\d+)/)?$', permission_required("sufix.add_contacts")(ContactCreate.as_view()), name="contacts_add"),
  url(r'^(?P<pk>\d+)/edit/$', permission_required("sufix.change_contacts")(ContactUpdate.as_view()), name="contacts_edit"),

)

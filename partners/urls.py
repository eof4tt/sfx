from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required, login_required
from partners.views import PartnerDetailView, PartnerCreate,PartnerUpdate
from . import views

urlpatterns = patterns('',
  url(r'^index/$', views.partners_list, name = "partners_index"),
  url(r'^(?P<pk>\d+)/$', permission_required("sufix.add_partners")(PartnerDetailView.as_view()), name = "partners_detail"),
  url(r'^add/$', permission_required("sufix.add_partners")(PartnerCreate.as_view()), name = "partners_add"),
  url(r'^(?P<pk>\d+)/edit/$', permission_required("sufix.change_partners")(PartnerUpdate.as_view()), name = "partners_edit"),
)

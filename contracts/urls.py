from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required, login_required
from contracts.views import ContractDetailView, ContractCreate, ContractUpdate
from . import views

urlpatterns = patterns('',
  url(r'^index/$', views.contracts_list, name = "contracts_index"),
  url(r'^files/$', views.doc4contracts_list, name = "contract_files"),
  url(r'^(?P<pk>\d+)/$', login_required(ContractDetailView.as_view()), name = "contracts_detail"),
  url(r'^add/$', permission_required("sufix.add_projects")(ContractCreate.as_view()), name = "contracts_add"),
  url(r'^(?P<pk>\d+)/edit/$', permission_required("sufix.change_projects")(ContractUpdate.as_view()), name = "contracts_edit"),
)

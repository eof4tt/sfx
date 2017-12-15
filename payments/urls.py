from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required, login_required
from payments.views import *
from . import views

urlpatterns = patterns('',
  url(r'^index/$', views.payments_list, name = "payments_index"),
  url(r'^(?P<pk>\d+)/$', permission_required("sufix.add_payments")(PaymentDetailView.as_view()), name = "payments_detail"),
  url(r'^add/(?:(?P<order>\d+)/)?$', permission_required("sufix.add_payments")(PaymentCreate.as_view()), name = "payments_add"),
  url(r'^(?P<pk>\d+)/edit/$', permission_required("sufix.change_payments")(PaymentUpdate.as_view()), name = "payments_edit"),
)

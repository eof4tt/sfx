from django.conf.urls import patterns, url
from django.contrib.auth.decorators import permission_required, login_required
from orders.views import OrderCreate, OrderUpdate, OrderDetailView
from . import views

urlpatterns = patterns('',
  url(r'^index/$', views.orders_list, name='orders_index'),
  url(r'^files/$', views.doc4orders_list, name='order_files'),
  url(r'^(?P<pk>\d+)/$', login_required(OrderDetailView.as_view()), name = "orders_detail"),
  url(r'^add/(?:(?P<contract>\d+)/)?$', permission_required("sufix.add_orders")(OrderCreate.as_view()), name = "orders_add"),
  url(r'^(?P<pk>\d+)/edit/$', permission_required("sufix.change_orders")(OrderUpdate.as_view()), name = "orders_edit"),
)

# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
#from cms.sitemaps import CMSSitemap
from django.conf import settings
from django.conf.urls import patterns,include, url
from django.conf.urls.static import static
from django.contrib import admin
#admin.autodiscover()
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from solid_i18n.urls import solid_i18n_patterns
from django.views import static
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .decorators import check_recaptcha
import os
#from django.conf.urls.i18n import i18n_patterns



urlpatterns = [
    #url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap',
    #    {'sitemaps': {'cmspages': CMSSitemap}}),
    #url(r'^select2/', include('django_select2.urls')),
    url(r'^accounts/login/$', views.LoginFormView.as_view(),name="login"),
    url(r'^login/$', check_recaptcha(views.LoginFormView.as_view()),name="login"),
    url(r'^logout/$', views.LogoutView.as_view(),name="logout"),
    #url(r'^registration/$', check_recaptcha(views.RegisterFormView.as_view()),name="registration"),
    url(r'^profile/$', views.get_user, name = "user_profile"),
    url(r'^contracts/', include('contracts.urls')),
    url(r'^orders/', include('orders.urls')),
    url(r'^partners/', include('partners.urls')),
    url(r'^contacts/', include('contacts.urls')),
    url(r'^payments/', include('payments.urls')),
    url(r'^cabinet_admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
#    url(r'^$', include('main.urls')),

]+staticfiles_urlpatterns()

#urlpatterns += solid_i18n_patterns('',
#    url(r'^admin/', include(admin.site.urls)),  # NOQA
#    url(r'^', include('cms.urls')),
#)

# This is only needed when using runserver.
if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns

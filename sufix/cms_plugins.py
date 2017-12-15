from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models import CMSPlugin
from django.utils.translation import ugettext as _
from .models import *
from django.shortcuts import render_to_response
from sufix.models import Projects, Contacts
from django.shortcuts import get_object_or_404, render, render_to_response

class ProjectsPlugin(CMSPluginBase):
    module = ("SUFIX Tables")
    name = ("Table Projects")
    render_template = "sufix/projects_plugin.html"

    def render(self, context, instance, placeholder):
        return context
plugin_pool.register_plugin(ProjectsPlugin)



class HelloPlugin(CMSPluginBase):
    model = CMSPlugin
    name = ("Hello Plugin")
    render_template = "sufix/hello_plugin.html"
    def render(self, context, instance, placeholder):
        return context
plugin_pool.register_plugin(HelloPlugin)


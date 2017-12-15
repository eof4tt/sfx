from django.views.generic.base import TemplateView

from generic.mixins import CategoryListMixin
from sufix.models import Projects

class MainPageView(TemplateView, CategoryListMixin):
  template_name = "mainpage.html"
  contracts = Projects.objects.filter(featured = True)

  def get_context_data(self, **kwargs):
    context = super(MainPageView, self).get_context_data(**kwargs)
    context["contracts"] = self.contracts
    return context

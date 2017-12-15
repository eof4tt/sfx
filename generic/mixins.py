from django.views.generic.base import ContextMixin

from sufix.models import ProjectType

class CategoryListMixin(ContextMixin):
  def get_context_data(self, **kwargs):
    context = super(CategoryListMixin, self).get_context_data(**kwargs)
    context["current_url"] = self.request.path
    context["categories"] = ProjectType.objects.all()
    return context

class PageNumberMixin(CategoryListMixin):
  def get_context_data(self, **kwargs):
    context = super(PageNumberMixin, self).get_context_data(**kwargs)
    try:
      context["pn"] = self.request.GET["page"]
    except KeyError:
      context["pn"] = "1"
    return context

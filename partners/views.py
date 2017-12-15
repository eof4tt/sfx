from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ProcessFormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.forms.models import inlineformset_factory
from django.forms import *

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404

# import logging

from sufix.models import Partners, PartnerDetails, PartnersDescriptions,Contacts
from sufix.models import Docs4Projects,DocStatus4Projects,DocStatusAdd4Projects,DocType4Projects,DocsDescription4Projects,Orders
from partners.forms import PartnerForm


# logger = logging.getLogger(__name__)

PartnerDetailsFormset = inlineformset_factory(Partners, PartnerDetails,
                                                can_delete=False, extra=1,
                                                fields='__all__',
                                                widgets={'details_of_bank': Textarea(attrs={'cols': 65, 'rows': 4}), }
                                              )

PartnerDescriptionFormset = inlineformset_factory(Partners, PartnersDescriptions,
                                                can_delete=False, extra=1,
                                                fields=['description'],
                                                widgets={'description': Textarea(attrs={'cols': 65, 'rows': 4}), }
                                                  )

PartnerContactsFormset = inlineformset_factory(Partners, Contacts,
                                                can_delete=True, extra=1,
                                                fields='__all__',
                                               )

def partners_list(request):
        if request.user.is_authenticated():
            # Авторизованный пользователь.
            partner = Partners.objects.all()
            return render(request, 'partners_index.html', {'partner': partner})  # Пользователь авторизован.
        else:
            # Анонимный пользователь.
            raise Http404("404")


class PartnerDetailView(DetailView):
  model = Partners
  template_name = "partner.html"
  def get_context_data(self, **kwargs):
      context = super(PartnerDetailView, self).get_context_data(**kwargs)
      context['contact_list'] = Contacts.objects.all()
      return context


class PartnerCreate(TemplateView):
    model = Partners
    template_name = "partner_add.html"
    form = None
    formset2detail = None
    formset2desc = None
    def get(self, request, *args, **kwargs):
        self.form = PartnerForm()
        self.formset2detail = PartnerDetailsFormset()
        self.formset2desc = PartnerDescriptionFormset()
        return super(PartnerCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PartnerCreate, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['formset2detail'] = self.formset2detail
        context['formset2desc'] = self.formset2desc
        return context

    def post(self, request, *args, **kwargs):
        self.form = PartnerForm(request.POST)
        if request.method == "POST":
            if self.form.is_valid():
                new_partner = self.form.save()
                self.formset2detail = PartnerDetailsFormset(request.POST, instance=new_partner)
                self.formset2desc = PartnerDescriptionFormset(request.POST, instance=new_partner)
                if self.formset2detail.is_valid():
                    if self.formset2desc.is_valid():
                            self.formset2desc.save()
                            self.formset2detail.save()
                            messages.add_message(request, messages.SUCCESS, "Контрагент успешно добавлен. ")
                            return redirect("/partners/index/", *args, **kwargs)
                else:
                    messages.add_message(request, messages.ERROR,
                                         "ОШИБКА при заполнении данных! Проверьте заполнение полей. ")
        self.formset2detail = PartnerDetailsFormset(request.POST)
        self.formset2desc = PartnerDescriptionFormset(request.POST)
        return super(PartnerCreate, self).get(request, *args, **kwargs)



class PartnerUpdate(TemplateView):
    model = Partners
    template_name = "partner_edit.html"

    def get(self, request, *args, **kwargs):
        self.partner = Partners.objects.get(pk=self.kwargs["pk"])
        self.form = PartnerForm(instance=self.partner)
        self.formset2detail = PartnerDetailsFormset(instance=self.partner)
        self.formset2desc = PartnerDescriptionFormset(instance=self.partner)
        return super(PartnerUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PartnerUpdate, self).get_context_data(**kwargs)
        context["partner"] = self.partner
        context["form"] = self.form
        context["formset2detail"] = self.formset2detail
        context["formset2desc"] = self.formset2desc
        return context

    def post(self, request, *args, **kwargs):
        self.partner = Partners.objects.get(pk=self.kwargs["pk"])
        if request.method == "POST":
            self.form = PartnerForm(request.POST, instance=self.partner)
            if self.form.is_valid():
                self.form.save()
                self.formset2detail = PartnerDetailsFormset(request.POST, instance=self.partner)
                self.formset2desc = PartnerDescriptionFormset(request.POST, instance=self.partner)
                messages.add_message(request, messages.SUCCESS, "Обновление данных произведено. ")
                if self.formset2detail.is_valid():
                    if self.formset2desc.is_valid():
                        self.formset2desc.save()
                        self.formset2detail.save()
                        messages.add_message(request, messages.SUCCESS, "Контрагент успешно изменен. ")
                        return redirect(reverse("partners_detail", kwargs={"pk": self.partner.pk}))

                else:
                    messages.add_message(request, messages.ERROR,
                                         "ОШИБКА при заполнении реквизитов! Проверьте заполнение обязательных полей. ")
            else:
                messages.add_message(request, messages.ERROR,
                                     "ВНИМАНИЕ: Необходимо заполнить все обязательные параметры! ")
            return super(PartnerUpdate, self).get(request, *args, **kwargs)
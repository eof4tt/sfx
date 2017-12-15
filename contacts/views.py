from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.edit import ProcessFormView
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.forms.models import inlineformset_factory
from django.forms import *

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404

# import logging

from sufix.models import Partners, Contacts, ContactDetails, ContactsDescriptions
from sufix.models import Docs4Projects,DocStatus4Projects,DocStatusAdd4Projects,DocType4Projects,DocsDescription4Projects,Orders
from contacts.forms import ContactsForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from sufix.decorators import group_required, email_required
# logger = logging.getLogger(__name__)

ContactDetailsFormset = inlineformset_factory(Contacts, ContactDetails,
                                                can_delete=False, extra=1,
                                                fields='__all__',
                                              )

ContactDescriptionFormset = inlineformset_factory(Contacts, ContactsDescriptions,
                                                can_delete=False, extra=1,
                                                fields=['description'],
                                                widgets={'description': Textarea(attrs={'cols': 65, 'rows': 2}), }
                                                  )
@group_required()
@email_required()
def  contacts_list(request):
    if request.user.is_authenticated():
        # Авторизованный пользователь.
        contact = Contacts.objects.all()
        perm_edit=request.user.has_perm('sufix.change_contacts')
        perm_add = request.user.has_perm('sufix.add_contacts')
        return render(request, 'contact_index.html', {'contact':contact, 'perm_add':perm_add, 'perm_edit':perm_edit})# Пользователь авторизован.
    else:
        # Анонимный пользователь.
        raise Http404("404")


class ContactDetailView(DetailView):
  model = Contacts
  template_name = "contact.html"
  def get(self, request, *args, **kwargs):
      if request.user.is_authenticated():
          # Авторизованный пользователь.
          self.perm_edit = request.user.has_perm('sufix.change_contacts')
          return super(ContactDetailView, self).get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
      context = super(ContactDetailView, self).get_context_data(**kwargs)
      context["perm_edit"]=self.perm_edit
      return context


class ContactCreate(TemplateView):
    model = Contacts
    template_name = "contact_add.html"
    form = None
    formset2detail = None
    formset2desc = None
    def get(self, request, *args, **kwargs):
        dataform={
            'partner': self.kwargs["prtnr"]
        }
        self.form = ContactsForm(initial=dataform)
        self.formset2detail = ContactDetailsFormset()
        #self.formset2desc = ContactDescriptionFormset()
        return super(ContactCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactCreate, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['formset2detail'] = self.formset2detail
        #context['formset2desc'] = self.formset2desc
        return context

    def post(self, request, *args, **kwargs):
        self.form = ContactsForm(request.POST)
        if request.method == "POST":
            if self.form.is_valid():
                new_contact = self.form.save()
                self.formset2detail = ContactDetailsFormset(request.POST, instance=new_contact)
                #self.formset2desc = ContactDescriptionFormset(request.POST, instance=new_contact)
                if self.formset2detail.is_valid():
                    #if self.formset2desc.is_valid():
                           # self.formset2desc.save()
                    self.formset2detail.save()
                    messages.add_message(request, messages.SUCCESS, "Контакт успешно добавлен. ")
                    return redirect("/contacts/index/", *args, **kwargs)
                else:
                    messages.add_message(request, messages.ERROR,
                                         "ОШИБКА при заполнении данных! Проверьте заполнение полей. ")
        self.formset2detail = ContactDetailsFormset(request.POST)
        self.formset2desc = ContactDescriptionFormset(request.POST)
        return super(ContactCreate, self).get(request, *args, **kwargs)


class ContactUpdate(TemplateView):
    model = Contacts
    template_name = "contact_edit.html"

    def get(self, request, *args, **kwargs):
        self.contact = Contacts.objects.get(pk=self.kwargs["pk"])
        self.form = ContactsForm(instance=self.contact)
        self.formset2detail = ContactDetailsFormset(instance=self.contact)
        self.formset2desc = ContactDescriptionFormset(instance=self.contact)
        return super(ContactUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ContactUpdate, self).get_context_data(**kwargs)
        context["contact"] = self.contact
        context["form"] = self.form
        context["formset2detail"] = self.formset2detail
        context["formset2desc"] = self.formset2desc
        return context

    def post(self, request, *args, **kwargs):
        self.contact = Contacts.objects.get(pk=self.kwargs["pk"])
        if request.method == "POST":
            self.form = ContactsForm(request.POST, instance=self.contact)
            if self.form.is_valid():
                self.form.save()
                self.formset2detail = ContactDetailsFormset(request.POST, instance=self.contact)
                self.formset2desc = ContactDescriptionFormset(request.POST, instance=self.contact)
                messages.add_message(request, messages.SUCCESS, "Обновление данных произведено. ")
                if self.formset2detail.is_valid():
                    if self.formset2desc.is_valid():
                        self.formset2desc.save()
                        self.formset2detail.save()
                        messages.add_message(request, messages.SUCCESS, "Контакт успешно изменен. ")
                        return redirect(reverse("contacts_detail", kwargs={"pk": self.contact.pk}))
                else:
                    messages.add_message(request, messages.ERROR,
                                         "ОШИБКА при заполнении реквизитов! Проверьте заполнение обязательных полей. ")
            else:
                messages.add_message(request, messages.ERROR,
                                     "ВНИМАНИЕ: Необходимо заполнить все обязательные параметры! ")
            return super(ContactUpdate, self).get(request, *args, **kwargs)
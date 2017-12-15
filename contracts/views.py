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

#from django.contrib.syndication.views import Feed
#from django.utils.feedgenerator import Atom1Feed
from django.core.exceptions import ObjectDoesNotExist
# import logging
from datetimewidget.widgets import DateTimeWidget, DateWidget
from sufix.models import Projects,ProjectType,ProjectStatus,ProjectsDescriptions,Partners
from sufix.models import Docs4Projects,DocStatus4Projects,DocStatusAdd4Projects,DocType4Projects,DocsDescription4Projects,Orders, Payments
from contracts.forms import ContractForm
from sufix.decorators import email_required
from generic.mixins import CategoryListMixin, PageNumberMixin
from generic.controllers import PageNumberView

from django.core.exceptions import ValidationError
import os
# logger = logging.getLogger(__name__)

ContractDocsFormset = inlineformset_factory(Projects, Docs4Projects,
                                            can_delete = True, extra=1, fk_name='project_name',
                                            fields = ['project_name','doc_name','reg_num','doc_date','type','status','status_add','doc_data'],
                                            widgets={'doc_name': TextInput(attrs={'size': 135}),
                                                    'reg_num': TextInput(attrs={'size': 10}),
                                                    'doc_date': DateWidget(attrs={'size': 9}, usel10n=True, bootstrap_version=3, options={'weekStart':1,'todayHighlight':True,'clearBtn': False,'pickerPosition':'bottom-left'}),
                                                     })
ContractDescriptionFormset = inlineformset_factory(Projects, ProjectsDescriptions,
                                                can_delete=False, extra=1,
                                                fields=['project_summ','description'],
                                                widgets={'description': Textarea(attrs={'cols': 65, 'rows': 4}), })

def contracts_list(request):
        if request.user.is_authenticated():
            if request.user.email == '':
                raise Http404("404")
            # Авторизованный пользователь.
            perm_edit = request.user.has_perm('sufix.change_projects')
            perm_add = request.user.has_perm('sufix.add_projects')
            contract = Projects.objects.all()
            return render(request, 'contracts_index.html', {'contract': contract, 'perm_add':perm_add, 'perm_edit':perm_edit})  # Пользователь авторизован.
        else:
            # Анонимный пользователь.
            raise Http404("404")

def doc4contracts_list(request):
    if request.user.is_authenticated():
        if request.user.email == '':
            raise Http404("404")
        # Авторизованный пользователь.
        perm_flink = request.user.has_perm('sufix.add_projects')
        contract = Projects.objects.all()
        doc4contract = Docs4Projects.objects.filter(project_name=contract)
        return render(request, 'contract_files.html',
                      {'contract': contract, 'doc4contract': doc4contract, 'perm_flink':perm_flink})  # Пользователь авторизован.
    else:
        # Анонимный пользователь.
        raise Http404("404")




class ContractCreate(TemplateView):
    model = Projects
    template_name = "contract_add.html"
    #cat = None
    form = None
    formset2file = None
    formset2desc = None
    success_url = "/contracts/index/"

    def get(self, request, *args, **kwargs):
        self.form = ContractForm()
        self.formset2desc = ContractDescriptionFormset()
        self.formset2files = ContractDocsFormset()
        return super(ContractCreate, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(ContractCreate, self).get_context_data(**kwargs)
        context["form"] = self.form
        context["formset2desc"] = self.formset2desc
        context["formset2files"] = self.formset2files
        return context
    def post(self, request, *args, **kwargs):
        self.form = ContractForm(request.POST, request.FILES)
        if request.method == "POST":
            if self.form.is_valid():
                new_contract = self.form.save()
                self.formset2files = ContractDocsFormset(request.POST, request.FILES, instance = new_contract)
                self.formset2desc = ContractDescriptionFormset(request.POST, request.FILES, instance=new_contract)
                messages.add_message(request, messages.SUCCESS, "Контракт успешно добавлен. ")
                if self.formset2desc.is_valid():
                    self.formset2desc.save()
                    messages.add_message(request, messages.SUCCESS, "Описане контракта успешно сохранено. ")
                    if self.formset2files.is_valid():
                        self.formset2files.save()
                        messages.add_message(request, messages.SUCCESS, "Документ(ы) к Контракту успешно добавлен(ы). ")
                        return redirect("/contracts/index/", *args, **kwargs)
                    else :
                        messages.add_message(request, messages.ERROR, "Проверьте корректность добавление нового документа или подтвердите текущие изменения. ")
                else:
                    messages.add_message(request, messages.ERROR, "Проверьте корректность заполнения Описания. ")
        self.formset2desc = ContractDescriptionFormset(request.POST, request.FILES)
        self.formset2files = ContractDocsFormset(request.POST, request.FILES)
        messages.add_message(request, messages.SUCCESS, "ВНИМАНИЕ: Необходимо заполнить все обязательные параметры")
        return super(ContractCreate, self).get(request, *args, **kwargs)

class ContractUpdate(TemplateView):
    model = Projects
    template_name = "contract_edit.html"
    success_url = "/contracts/index/"

    def get(self, request, *args, **kwargs):
        self.contract = Projects.objects.get(pk= self.kwargs["pk"])
        self.form = ContractForm(instance=self.contract)
        self.formset2desc = ContractDescriptionFormset(instance=self.contract)
        self.formset2files = ContractDocsFormset(instance=self.contract)
        return super(ContractUpdate,self).get(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super(ContractUpdate, self).get_context_data(**kwargs)
        context["contract"] = self.contract
        context["form"] = self.form
        context["formset2desc"] = self.formset2desc
        context["formset2files"] = self.formset2files
        return context
    def post(self, request, *args, **kwargs):
        self.contract = Projects.objects.get(pk=self.kwargs["pk"])
        if request.method == "POST":
            self.form = ContractForm(request.POST, request.FILES,instance=self.contract)
            self.formset2desc = ContractDescriptionFormset(request.POST, request.FILES, instance=self.contract)
            self.formset2files = ContractDocsFormset(request.POST, request.FILES, instance=self.contract)
            if self.form.is_valid() :
                self.form.save()
                messages.add_message(request, messages.SUCCESS, "Контракт успешно изменен. ")
                if self.formset2desc.is_valid() :
                    self.formset2desc.save()
                    messages.add_message(request, messages.SUCCESS, "Описание контракта успешно сохранено. ")
                    if self.formset2files.is_valid():
                        self.formset2files.save()
                        messages.add_message(request, messages.SUCCESS, "Документ успешно изменен! ")
                        return redirect(reverse("contracts_detail", kwargs={"pk": self.contract.pk}))
                    else :
                        messages.add_message(request, messages.ERROR, "Проверьте корректность добавление нового документа или подтвердите текущие изменения. ")
                else:
                    messages.add_message(request, messages.ERROR, "Проверьте корректность заполнения Описания. ")

        messages.add_message(request, messages.ERROR, "ВНИМАНИЕ: Необходимо заполнить все обязательные параметры")
        return super(ContractUpdate,self).get(request,*args,**kwargs)


class ContractDetailView(DetailView):
  model = Projects
  template_name = "contract.html"
  def get(self, request, *args, **kwargs):
      if request.user.is_authenticated():
          if request.user.email == '':
              raise Http404("404")
          # Авторизованный пользователь.
          self.perm_edit = request.user.has_perm('sufix.change_projects')
          return super(ContractDetailView, self).get(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
      context = super(ContractDetailView, self).get_context_data(**kwargs)
      context["perm_edit"] = self.perm_edit
      #####
      ssumm = 0
      payinsumm = 0
      payoutsumm = 0
      contract = Projects.objects.get(pk=self.kwargs["pk"])
      cntrct_order = Orders.objects.filter(project_name=contract)
      for cntrct_order in cntrct_order:
          ssumm += cntrct_order.ordersdescription.order_summ

          ord_payin = Payments.objects.filter(order_name=cntrct_order,status_id=3, intention__pay_type_id=1)
          for ord_payin in ord_payin:
              payinsumm += ord_payin.paydetails.pay_summ

          ord_payout = Payments.objects.filter(order_name=cntrct_order,status_id=3, intention__pay_type_id=2)
          for ord_payout in ord_payout:
              payoutsumm +=ord_payout.paydetails.pay_summ
      context['orders_summ'] = ssumm

      psumm=contract.projectsdescriptions.project_summ


      if psumm == 0 or psumm == None:
          context['orders_used'] = round(0)
      else:
          context['orders_used'] = round(ssumm / psumm * 100)
      context['orders_payinsumm'] = payinsumm
      context['orders_payoutsumm'] = payoutsumm
      if payinsumm==0:
          context['orders_finperformance_in'] = round(0)
          context['orders_finperformance'] = round(-100)
      else:
        context['orders_finperformance_in'] = round(payinsumm/ssumm*100)
        if payoutsumm==0:
            context['orders_finperformance_out'] = round(0)
            context['orders_finperformance'] = round(100-(payoutsumm/payinsumm*100))
        else:
            context['orders_finperformance_out'] = round(payoutsumm/payinsumm*100)
            context['orders_finperformance'] = round(100-(payoutsumm/payinsumm*100))
      context['orders_finperformance_summ'] = payinsumm-payoutsumm
      #####
      context['order_list'] = Orders.objects.all()
      context['payment_list'] = Payments.objects.all()
      context['doc_list'] = Docs4Projects.objects.all()
      return context





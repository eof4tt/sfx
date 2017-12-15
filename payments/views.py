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
from sufix.models import Payments, PayDetails, PaymentsDescription, Docs4Payments
from payments.forms import PaymentsForm, PaymentsEditForm
from datetimewidget.widgets import DateTimeWidget, DateWidget
from sufix.decorators import group_required, email_required

# logger = logging.getLogger(__name__)

PaymentDocsFormset = inlineformset_factory(Payments, Docs4Payments,
                                         can_delete=True, extra=1, fk_name='payment_name',
                                         fields=['payment_name', 'doc_name', 'reg_num' ,'doc_date', 'type', 'status', 'status_add',
                                                 'doc_data'],
                                         widgets={'doc_name': TextInput(attrs={'size': 135}),
                                                  'reg_num': TextInput(attrs={'size': 10}),
                                                  'doc_date': DateWidget(attrs={'size': 9}, usel10n=True, bootstrap_version=3, options={'weekStart':1,'todayHighlight':True,'clearBtn': False,'pickerPosition':'bottom-left'}),
                                         })

PaymentDescriptionFormset = inlineformset_factory(Payments, PaymentsDescription,
                                                can_delete=False, extra=1,
                                                fields=['description'],
                                                widgets={'description': Textarea(attrs={'cols': 65, 'rows': 4}),})

PaymentDetailFormset = inlineformset_factory(Payments, PayDetails,
                                                can_delete=False, extra=1, fk_name='payment',
                                                fields=['pay_summ', 'pay_vat_size', 'pay_vat_summ', 'pay_total_summ'],
                                                widgets={
                                                        'pay_summ': TextInput(attrs={'size': 72}),
                                                        'pay_vat_size': Select(attrs={'style':'width: 150px'}),
                                                        'pay_vat_summ': TextInput(attrs={'size': 47, 'readonly':'readonly'}),
                                                        'pay_total_summ': TextInput(attrs={'size': 72, 'readonly':'readonly'}),
                                                }
                                             )
#class PaymentCreate

class PaymentCreate(TemplateView):
    model = Payments
    template_name = "payment_add.html"
    form = None
    formset2detail = None
    formset2desc = None
    formset2files = None
    success_url = "/payments/index/"

    def get(self, request, *args, **kwargs):
        dataform={
            'order_name': self.kwargs["order"]
        }
        self.form = PaymentsForm(initial=dataform)
        self.formset2detail = PaymentDetailFormset()
        self.formset2desc = PaymentDescriptionFormset()
        self.formset2files = PaymentDocsFormset()
        return super(PaymentCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentCreate, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['formset2detail'] = self.formset2detail
        context['formset2desc'] = self.formset2desc
        context['formset2files'] = self.formset2files
        return context

    def post(self, request, *args, **kwargs):
        self.form = PaymentsForm(request.POST, request.FILES)
        if request.method == "POST":
            if self.form.is_valid():
                new_payment = self.form.save()
                self.formset2detail = PaymentDetailFormset(request.POST, request.FILES, instance=new_payment)
                self.formset2desc = PaymentDescriptionFormset(request.POST, request.FILES, instance=new_payment)
                self.formset2files = PaymentDocsFormset(request.POST, request.FILES, instance=new_payment)
                if self.formset2detail.is_valid():
                    if self.formset2desc.is_valid():
                        if self.formset2files.is_valid():
                            self.formset2files.save()
                            self.formset2desc.save()
                            self.formset2detail.save()
                            messages.add_message(request, messages.SUCCESS, "Финансовая операция успешно добавлена. ")
                            return redirect("/payments/index/", *args, **kwargs)
                        else:
                            messages.add_message(request, messages.ERROR, "ОШИБКА при добавлении файла! Проверьте заполнение полей. ")
                else:
                    messages.add_message(request, messages.ERROR,
                                         "ОШИБКА при заполнении Суммы операции! Проверьте заполнение полей. ")
        self.formset2detail = PaymentDetailFormset(request.POST, request.FILES)
        self.formset2desc = PaymentDescriptionFormset(request.POST, request.FILES)
        self.formset2files = PaymentDocsFormset(request.POST, request.FILES)
        return super(PaymentCreate, self).get(request, *args, **kwargs)


class PaymentUpdate(TemplateView):
    model = Payments
    template_name = "payment_edit.html"
    success_url = "/payments/index/"

    def get(self, request, *args, **kwargs):
        self.payment = Payments.objects.get(pk=self.kwargs["pk"])
        self.form = PaymentsEditForm(instance=self.payment)
        self.formset2detail = PaymentDetailFormset(instance=self.payment)
        self.formset2desc = PaymentDescriptionFormset(instance=self.payment)
        self.formset2files = PaymentDocsFormset(instance=self.payment)
        return super(PaymentUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentUpdate, self).get_context_data(**kwargs)
        context["payment"] = self.payment
        context["form"] = self.form
        context["formset2detail"] = self.formset2detail
        context["formset2desc"] = self.formset2desc
        context["formset2files"] = self.formset2files
        return context

    def post(self, request, *args, **kwargs):
        self.payment = Payments.objects.get(pk=self.kwargs["pk"])
        if request.method == "POST":
            self.form = PaymentsEditForm(request.POST, instance=self.payment)
            if self.form.is_valid():
                self.form.save()
                self.formset2detail = PaymentDetailFormset(request.POST, instance=self.payment)
                self.formset2desc = PaymentDescriptionFormset(request.POST, instance=self.payment)
                self.formset2files = PaymentDocsFormset(request.POST, request.FILES, instance=self.payment)
                messages.add_message(request, messages.SUCCESS, "Обновление данных произведено. ")
                if self.formset2detail.is_valid():
                    if self.formset2desc.is_valid():
                        if self.formset2files.is_valid():
                            self.formset2desc.save()
                            self.formset2detail.save()
                            self.formset2files.save()
                            messages.add_message(request, messages.SUCCESS, "Финансовая операция успешно изменена. ")
                            return redirect(reverse("payments_detail", kwargs={"pk": self.payment.pk}))
                        else :
                            messages.add_message(request, messages.ERROR,
                                                 "ОШИБКА при добавлении файла! Проверьте заполнение полей. ")
                else:
                    messages.add_message(request, messages.ERROR,
                                         "ОШИБКА при заполнении Суммы операции! Проверьте заполнение полей. ")
            else:
                messages.add_message(request, messages.ERROR,"ВНИМАНИЕ: Необходимо заполнить все обязательные параметры! ")
            return super(PaymentUpdate, self).get(request, *args, **kwargs)


class PaymentDetailView(DetailView):
    model = Payments
    template_name = "payment.html"
    def get_context_data(self, **kwargs):
        context = super (PaymentDetailView,self).get_context_data(**kwargs)
        context['doc_list'] = Docs4Payments.objects.all()
        return context

@group_required()
@email_required()
def  payments_list(request):
    if request.user.is_authenticated():
        # Авторизованный пользователь.
        perm_edit = request.user.has_perm('sufix.change_payments')
        perm_add = request.user.has_perm('sufix.add_payments')
        payment = Payments.objects.all()
        details = PayDetails.objects.filter(payment=payment)
        return render(request, 'payments_index.html', {'payment': payment, 'details':details, 'perm_edit':perm_edit, 'perm_add':perm_add})  # Пользователь авторизован.
    else:
        # Анонимный пользователь.
        raise Http404("404")

def doc4payments_list(request):
    if request.user.is_authenticated():
        # Авторизованный пользователь.
        payment = Payments.objects.all()
        doc4payment = Docs4Payments.objects.filter(pay_name=payment)
        return render(request, 'payment_files.html',
                      {'payment': payment, 'doc4payment': doc4payment})  # Пользователь авторизован.
    else:
        # Анонимный пользователь.
        raise Http404("404")

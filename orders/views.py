from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
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
# from django.contrib.syndication.views import Feed
# from django.utils.feedgenerator import Atom1Feed
from django.core.exceptions import ObjectDoesNotExist
# import logging
from sufix.models import Projects, ProjectType, ProjectStatus, ProjectsDescriptions
from sufix.models import Orders, OrderStatus, OrderType, OrdersDescription, OrderNomenclature, Docs, Payments
from orders.forms import OrderForm,OrderEditForm
from generic.mixins import CategoryListMixin, PageNumberMixin
from generic.controllers import PageNumberView
from datetimewidget.widgets import DateTimeWidget, DateWidget
from sufix.decorators import email_required

OrderDocsFormset = inlineformset_factory(Orders, Docs,
                                         can_delete=True, extra=1, fk_name='order_name',
                                         fields=['order_name', 'doc_name', 'reg_num' ,'doc_date', 'type', 'status', 'status_add',
                                                 'doc_data'],
                                         widgets={'doc_name': TextInput(attrs={'size': 135}),
                                                  'reg_num': TextInput(attrs={'size': 10}),
                                                  'doc_date': DateWidget(attrs={'size': 9}, usel10n=True, bootstrap_version=3, options={'weekStart':1,'todayHighlight':True,'clearBtn': False,'pickerPosition':'bottom-left'}),
                                                  })
OrderDescriptionFormset = inlineformset_factory(Orders, OrdersDescription,
                                                can_delete=False, extra=1,
                                                fields=['order_summ','description'],
                                                widgets={'description': Textarea(attrs={'cols': 65, 'rows': 4}), })



class OrderCreate(TemplateView):
    model = Orders
    template_name = "order_add.html"
    form = None
    formset2files = None
    formset2desc = None
    success_url = "/orders/index/"

    def get(self, request, *args, **kwargs):
        dataform={
            'project_name': self.kwargs["contract"]
        }
        self.form = OrderForm(initial=dataform)
        self.formset2desc = OrderDescriptionFormset()
        self.formset2files = OrderDocsFormset()
        return super(OrderCreate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderCreate, self).get_context_data(**kwargs)
        context['form'] = self.form
        context['formset2desc'] = self.formset2desc
        context['formset2files'] = self.formset2files
        return context

    def post(self, request, *args, **kwargs):
        self.form = OrderForm(request.POST, request.FILES)
        if request.method == "POST":
            if self.form.is_valid():
                new_order = self.form.save()
                self.formset2desc = OrderDescriptionFormset(request.POST, instance=new_order)
                self.formset2files = OrderDocsFormset(request.POST, request.FILES, instance=new_order)
                messages.add_message(request, messages.SUCCESS, "Заказ успешно добавлен. ")
                if self.formset2desc.is_valid():
                    self.formset2desc.save()
                    messages.add_message(request, messages.SUCCESS, "Описание успешно добавлено. ")
                    if self.formset2files.is_valid():
                        self.formset2files.save()
                        messages.add_message(request, messages.SUCCESS, "Документ(ы) к заказу успешно добавлен(ы). ")
                        return redirect("/orders/index/", *args, **kwargs)
                    else :
                        messages.add_message(request, messages.SUCCESS, "Проверьте корректность добавление нового документа или подтвердите текущие изменения. ")

        self.formset2desc = OrderDescriptionFormset(request.POST)
        self.formset2files = OrderDocsFormset(request.POST, request.FILES)
        messages.add_message(request, messages.SUCCESS, "ВНИМАНИЕ: Необходимо заполнить все обязательные параметры! ")
        return super(OrderCreate, self).get(request, *args, **kwargs)




class OrderUpdate(TemplateView):
    model = Orders
    template_name = "order_edit.html"
    success_url = "/orders/index/"

    def get(self, request, *args, **kwargs):
        self.order = Orders.objects.get(pk=self.kwargs["pk"])
        self.form = OrderEditForm(instance=self.order)
        self.formset2desc = OrderDescriptionFormset(instance=self.order)
        self.formset2files = OrderDocsFormset(instance=self.order)
        return super(OrderUpdate, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(OrderUpdate, self).get_context_data(**kwargs)
        context["order"] = self.order
        context["form"] = self.form
        context["formset2desc"] = self.formset2desc
        context["formset2files"] = self.formset2files
        return context

    def post(self, request, *args, **kwargs):
        self.order = Orders.objects.get(pk=self.kwargs["pk"])
        if request.method == "POST":
            self.form = OrderEditForm(request.POST, instance=self.order)
            if self.form.is_valid():
                self.form.save()
                messages.add_message(request, messages.SUCCESS, "Заказ успешно обновлен. ")
                self.formset2desc = OrderDescriptionFormset(request.POST, instance=self.order)
                self.formset2files = OrderDocsFormset(request.POST, request.FILES, instance=self.order)
                if self.formset2desc.is_valid():
                    if self.formset2files.is_valid():
                        self.formset2desc.save()
                        messages.add_message(request, messages.SUCCESS, "Описание успешно обновлено. ")
                        self.formset2files.save()
                        messages.add_message(request, messages.SUCCESS, "Список документов успешно обновлен. ")
                        return redirect(reverse("orders_detail", kwargs={"pk": self.order.pk}))
                    else :
                        messages.add_message(request, messages.ERROR,"Проверьте корректность добавление нового документа или подтвердите текущие изменения. ")
                else:
                    messages.add_message(request, messages.ERROR,"Проверьте корректность заполнения Описания ")
            else:
                messages.add_message(request, messages.ERROR,"ВНИМАНИЕ: Необходимо заполнить все обязательные параметры! ")
            return super(OrderUpdate, self).get(request, *args, **kwargs)




class OrderDetailView(DetailView):
    model = Orders
    template_name = "order.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            # Авторизованный пользователь.
            if request.user.email == '':
                raise Http404("404")
            self.perm_edit = request.user.has_perm('sufix.change_orders')
            return super(OrderDetailView, self).get(request, *args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super(OrderDetailView,self).get_context_data(**kwargs)
        context["perm_edit"] = self.perm_edit
        #####
        payinsumm = 0
        payoutsumm = 0
        #contract = Projects.objects.get(pk=self.kwargs["pk"])
        order = Orders.objects.get(pk=self.kwargs["pk"])
        ssumm = order.ordersdescription.order_summ
        ord_payin = Payments.objects.filter(order_name=order, status_id=3, intention__pay_type_id=1)
        for ord_payin in ord_payin:
            payinsumm += ord_payin.paydetails.pay_summ
        ord_payout = Payments.objects.filter(order_name=order, status_id=3, intention__pay_type_id=2)
        for ord_payout in ord_payout:
            payoutsumm += ord_payout.paydetails.pay_summ
        context['orders_summ'] = ssumm
        context['orders_payinsumm'] = payinsumm
        context['orders_payoutsumm'] = payoutsumm
        if payinsumm == 0 or payinsumm == None:
            context['orders_used'] = round(0)
            context['orders_finperformance_in'] = round(0)
            context['orders_finperformance'] = round(-100)
            context['orders_outused'] = round(payoutsumm * 100, 0)
        else:
            context['orders_used'] = round(payinsumm / ssumm * 100, 0)
            context['orders_outused'] = round(payoutsumm / payinsumm * 100, 0)
            context['orders_finperformance_in'] = round(payinsumm / ssumm * 100)
            if payoutsumm == 0:
                context['orders_finperformance_out'] = round(0)
                context['orders_finperformance'] = round(100 - (payoutsumm / payinsumm * 100))
            else:
                context['orders_finperformance_out'] = round(payoutsumm / payinsumm * 100)
                context['orders_finperformance'] = round(100 - (payoutsumm / payinsumm * 100))
        context['orders_finperformance_summ'] = payinsumm - payoutsumm
        #####
        context['doc_list'] = Docs.objects.all()
        context['payment_list'] = Payments.objects.all()
        return context

def orders_list(request):
    if request.user.is_authenticated():
        if request.user.email == '':
            raise Http404("404")
        perm_edit = request.user.has_perm('sufix.change_orders')
        perm_add = request.user.has_perm('sufix.add_orders')
        # Авторизованный пользователь.
        order = Orders.objects.all()
        doc2order = Docs.objects.filter(order_name=order)
        return render(request, 'orders_index.html',
                      {'order': order, 'doc2order': doc2order, 'perm_add':perm_add, 'perm_edit':perm_edit})  # Пользователь авторизован.
    else:
        # Анонимный пользователь.
        raise Http404("404")

def doc4orders_list(request):
    if request.user.is_authenticated():
        if request.user.email == '':
            raise Http404("404")
        # Авторизованный пользователь.
        perm_flink = request.user.has_perm('sufix.add_orders')
        order = Orders.objects.all()
        doc4order = Docs.objects.filter(order_name=order)
        return render(request, 'order_files.html',
                      {'order': order, 'doc4order': doc4order,'perm_flink':perm_flink})  # Пользователь авторизован.
    else:
        # Анонимный пользователь.
        raise Http404("404")



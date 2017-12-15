from django import forms
from django.forms import Textarea, Select
from django.db.models import Q
from datetimewidget.widgets import DateTimeWidget, DateWidget

from sufix.models import Payments,Orders

class PaymentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentsForm, self).__init__(*args, **kwargs)
        self.fields['order_name'].queryset = Orders.objects.filter(Q(status_id='3')|Q(status_id='6'))

    class Meta:
        model=Payments
        #exclude = ['payment_name']
        fields = '__all__'
        dateOptions = {
            'format': 'dd.mm.yyyy',
            'autoclose': True,
            'showMeridian': False,
            'weekStart': 1,
            'minView': 2,
            'maxView': 4,
            'clearBtn': False,
            'todayHighlight': True,
            'pickerPosition': 'bottom-left',
        }
        widgets = {
            'pay_date': DateWidget(options=dateOptions, usel10n=True, bootstrap_version=3),
        }
class PaymentsEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentsEditForm, self).__init__(*args, **kwargs)
        self.fields['order_name'].queryset = Orders.objects.filter(Q(status_id='3')|Q(status_id='6'))

    class Meta:
        model=Payments
        #exclude = ['payment_name']
        fields = '__all__'
        dateOptions = {
            'format': 'dd.mm.yyyy',
            'autoclose': True,
            'showMeridian': False,
            'weekStart': 1,
            'minView': 2,
            'maxView': 4,
            'clearBtn': False,
            'todayHighlight': True,
            'pickerPosition': 'bottom-left',
        }
        widgets = {
            'order_name': Select(attrs={'readonly':True}),
            'pay_date': DateWidget(options=dateOptions, usel10n=True, bootstrap_version=3),
        }

    def clean_order_name(self):
        instance=getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.order_name
        else:
            return self.cleaned_data['order_name']

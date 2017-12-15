from django import forms
from sufix.models import Projects,Orders,Partners
from django.forms import TextInput,Textarea,Select, DateInput
from datetimewidget.widgets import DateTimeWidget, DateWidget



class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].queryset = Projects.objects.filter(status_id=4)
        self.fields['subcontractor_name'].queryset = Partners.objects.filter(type=3, status_id=1)
    class Meta:
        model=Orders
        exclude=['nomenclature']
        fields = ['project_name','order_name','subcontractor_name','type','status','date_in','date_out','date_inreal','date_outreal','date_closed']
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
            'order_name': Textarea(attrs={'cols': 88, 'rows': 2}),
            'date_in': DateWidget(options=dateOptions, usel10n = True, bootstrap_version=3),
            'date_out': DateWidget(options=dateOptions, usel10n = True, bootstrap_version=3),
            'date_inreal': DateWidget(options=dateOptions, usel10n = True, bootstrap_version=3),
            'date_outreal': DateWidget(options=dateOptions, usel10n = True, bootstrap_version=3),
            'date_closed': DateWidget(options=dateOptions, usel10n = True, bootstrap_version=3),

        }
class OrderEditForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderEditForm, self).__init__(*args, **kwargs)
        self.fields['project_name'].queryset = Projects.objects.filter(status_id=4)
        self.fields['subcontractor_name'].queryset = Partners.objects.filter(type=3, status_id=1)

    class Meta:
        model=Orders
        exclude=['nomenclature']
        fields = ['project_name','order_name','subcontractor_name','type','status','date_in','date_out','date_inreal','date_outreal','date_closed']
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
            'order_name': Textarea(attrs={'cols': 88, 'rows': 2}),
            'project_name': Select(attrs={'readonly':True}),
            'date_in': DateInput(attrs={'readonly':True}),
            'date_out': DateInput(attrs={'readonly':True}),
            'date_inreal': DateWidget(options=dateOptions, usel10n=True, bootstrap_version=3),
            'date_outreal': DateWidget(options=dateOptions, usel10n=True, bootstrap_version=3),
            'date_closed': DateWidget(options=dateOptions, usel10n=True, bootstrap_version=3),
        }

    def clean_project_name(self):
        instance=getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.project_name
        else:
            return self.cleaned_data['project_name']
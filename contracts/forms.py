from django import forms
from django.forms import Textarea, Select
#from bootstrap3_datetime.widgets import DateTimePicker
#from django_bootstrap_datetimepicker.widgets import BootstrapDateTimeInput
from datetimewidget.widgets import DateTimeWidget, DateWidget
#from bootstrap3_datepicker.widgets import DatePickerInput
from sufix.models import Projects,Partners



class ContractForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self.fields['project_to_partner'].queryset = Partners.objects.filter(type=2,status_id=1)
    class Meta:
        model=Projects
        #exclude=['date_closed']
        fields = '__all__'
        dateOptions = {
            'format': 'dd.mm.yyyy',
            'autoclose': True,
            'showMeridian': False,
            'weekStart':1,
            'minView': 2,
            'maxView': 4,
            'clearBtn': False,
            'todayHighlight': True,
            'pickerPosition':'bottom-left',
        }

        widgets = {
            'project_name': Textarea(attrs={'cols': 88, 'rows': 2}),
            'project_shortname': Textarea(attrs={'cols': 44, 'rows': 1}),
            'date_in': DateWidget(options = dateOptions, usel10n = True, bootstrap_version=3),
            'date_out': DateWidget(options=dateOptions, usel10n = True, bootstrap_version=3),
            'date_closed': DateWidget(options=dateOptions, usel10n = True, bootstrap_version=3),
        }


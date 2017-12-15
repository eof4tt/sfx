from django import forms
from django.forms import Textarea, Select


from sufix.models import Contacts, Partners

class ContactsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactsForm, self).__init__(*args, **kwargs)
        self.fields['partner'].queryset = Partners.objects.filter(status_id=1)
    class Meta:
        model=Contacts
        fields = '__all__'

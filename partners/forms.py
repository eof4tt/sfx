from django import forms
from django.forms import Textarea, Select


from sufix.models import Partners

class PartnerForm(forms.ModelForm):
    class Meta:
        model=Partners
        fields = '__all__'

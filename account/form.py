from dataclasses import field
from django.forms import ModelForm
from catalog.models import SubList

class SublistItemDeleteForm(ModelForm):
    class Meta:
        model = SubList
        fields = '__all__'
    
class SubListItemUpdateForm(ModelForm):
    class Meta:
        model = SubList
        fields = '__all__'

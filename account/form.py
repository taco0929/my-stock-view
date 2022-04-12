from dataclasses import field
from django.forms import ModelForm
from catalog.models import SubList,UserLineID

class SublistItemDeleteForm(ModelForm):
    class Meta:
        model = SubList
        fields = '__all__'
    
class SubListItemUpdateForm(ModelForm):
    class Meta:
        model = SubList
        fields = '__all__'
        
class UserLineIdUpdateForm(ModelForm):
    class Meta:
        model = UserLineID
        fields ='__all__'
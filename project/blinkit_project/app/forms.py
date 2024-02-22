from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
  class Meta:
    model = ShippingAddress
    fields = ['building_name',
    'street','landmark','city',
    'state','zipcode']

class SetDeliveryAddressForm(forms.Form):
  delivery_address = forms.CharField()
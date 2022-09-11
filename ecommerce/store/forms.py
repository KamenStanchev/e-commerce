from ecommerce.store.models import Customer, ShippingAddress
from django import forms


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'name..'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email..'})
        }


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'country', 'zipcode', 'city']

        widgets = {
            'address': forms.TextInput(attrs={'placeholder': 'address...'}),
            'country': forms.TextInput(attrs={'placeholder': 'country...'}),
            'zipcode': forms.TextInput(attrs={'placeholder': 'zipcode...'}),
            'city': forms.TextInput(attrs={'placeholder': 'city...'})
        }


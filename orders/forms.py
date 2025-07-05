from django import forms
from .models import Order

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['transaction_number']
        widgets = {
            'transaction_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Transaction ID'}),
        }

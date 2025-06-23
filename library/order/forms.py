from django import forms
from .models import Order
from book.models import Book

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['book']
        labels = {
            'book': 'Select Book',
        } 
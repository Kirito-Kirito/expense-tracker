from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'transport': forms.Select(attrs={'class': 'form-select'}),
            'start_location': forms.TextInput(attrs={'class': 'form-control'}),
            'end_location': forms.TextInput(attrs={'class': 'form-control'}),
            'trip_type': forms.Select(attrs={'class': 'form-select'}),
            'purpose': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
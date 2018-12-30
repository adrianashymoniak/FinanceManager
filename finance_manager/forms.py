from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Transaction


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class CategoryForm(forms.ModelForm):
    category_name = forms.CharField(max_length=150, required=True, help_text='Please add category name')
    category_description = forms.CharField(max_length=250, required=False, help_text='Optional')

    class Meta:
        model = Category

        fields = (
            'category_name',
            'category_description',
        )


class TransactionForm(forms.ModelForm):
    type_of_operation = forms.CharField(max_length=30)
    amount = forms.DecimalField(max_digits=6, decimal_places=2)
    operation_date = forms.DateField()
    transaction_description = forms.CharField(max_length=250)
    category = forms.ModelChoiceField(queryset=Category.objects.all())

    class Meta:
        model = Transaction

        fields = (
            'type_of_operation',
            'amount',
            'operation_date',
            'transaction_description',
            'category',
        )

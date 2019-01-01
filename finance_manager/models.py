import datetime

from django.db import models


class Category(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None)
    category_name = models.CharField(max_length=150)
    category_description = models.CharField(max_length=250)


class Transaction(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, default=None)
    type_of_operation = models.CharField(max_length=8, choices=(
        ('Revenue', 'revenue'), ('Expenses', 'expenses')))
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    operation_date = models.DateField(default=datetime.date.today, blank=True)
    transaction_description = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.SET(None))

from django.contrib import admin
from .models import Category, Transaction

admin.register(Category, Transaction)(admin.ModelAdmin)

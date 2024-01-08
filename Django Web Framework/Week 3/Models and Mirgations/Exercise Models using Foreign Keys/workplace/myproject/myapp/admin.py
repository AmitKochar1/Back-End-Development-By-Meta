from django.contrib import admin
# Import the models from models.py
from . import models  
# Register your models here.
admin.site.register(models.DrinksCategory)
admin.site.register(models.Drinks)
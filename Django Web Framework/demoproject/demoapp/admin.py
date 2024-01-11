from django.contrib import admin
from .models import Reservation
# Register your models here.
@admin.register(Reservation)

class PersonAdmin(admin.ModelAdmin):
    list_display=('name', 'contact', 'time_log', 'count', 'notes')
    search_fields=('first_name__startswith', )
# admin.site.register(Logger)
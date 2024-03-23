from django import forms
from myapp.models import Booking

class BookingForm(forms.ModelForm):
    class Meta():
        Model = Booking
        Field = "__all__"
        
    
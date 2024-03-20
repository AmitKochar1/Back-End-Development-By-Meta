from django import forms
from myapp.models import Booking

class Bookingform(forms.ModelForm):
    class Meta():
        Model = Booking
        Field = "__all__"
        
    
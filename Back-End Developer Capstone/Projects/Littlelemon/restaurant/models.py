from django.db import models

# Create your models here.
class Booking(models.Model):
    name = models.CharField(max_length = 255)
    no_of_guest = models.IntegerField(default = 5)
    bookingdate = models.DateField()
    
    def __self__(self):
        return self.Name
    
class Menu(models.Model):
    title = models.CharField(max_length = 200)
    price = models.IntegerField()
    inventory = models.SmallIntegerField()
    
    def __str__(self):
        return f'{self.title} : {str(self.price)}'